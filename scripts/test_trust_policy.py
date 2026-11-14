"""Owner trust, ambiguous UI and cross-workspace regressions with fake Herdr."""
import json, os, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from load_config import resolve, native_args, expand_layout
from trust_policy import set_project, policy_for
from start_seat import dismiss_codex_trust, find_live_agent
from herdr_cli import HerdrError


class TrustPolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.registry=self.root/'owner.json'
        self.env=patch.dict(os.environ,{'WORKFLOW_HERDR_TRUST_FILE':str(self.registry)})
        self.env.start();self.addCleanup(self.env.stop)

    def test_full_trust_is_exact_root_and_not_repo_self_authorization(self):
        (self.root/'.herdr').mkdir()
        (self.root/'.herdr/workflow.yaml').write_text('security:\n  full_trust: true\n  auto_confirm_workspace: true\n')
        assert not resolve(self.root)['security']['full_trust']
        set_project(self.root,full_trust=True,auto_confirm=True)
        config=resolve(self.root)
        assert '--dangerously-bypass-approvals-and-sandbox' in native_args(config,'orchestrator',1,'case')
        assert 'dangerous' in native_args(config,'worker',1,'case')
        child=self.root/'child';child.mkdir()
        assert not policy_for(child)['full_trust']
        set_project(self.root,full_trust=False,auto_confirm=False,revoke=True)
        assert not policy_for(self.root)['full_trust']

    def test_ambiguous_or_unauthorized_trust_never_sends_keys(self):
        for authorized,screen in [(False,'Do you trust the contents of this directory?\n› 1. Yes, continue\n2. No, quit'),(True,'Do you trust the contents of this directory?\n1. Yes, continue\n› 2. No, quit')]:
            calls=[]
            def fake(args):
                calls.append(args);return {'text':screen}
            result=dismiss_codex_trust(kind='codex',name='worker',session=None,machine=None,runner=fake,sleep=lambda _:None,authorized=authorized,timeout_ms=1)
            assert not result['trust_cleared']
            assert not any('send-keys' in c for c in calls)

    def test_authorized_selected_yes_still_requires_composer(self):
        screens=iter(['Do you trust the contents of this directory?\n› 1. Yes, continue\n2. No, quit','Ask Codex to do anything'])
        calls=[]
        def fake(args):
            calls.append(args)
            return {'text':next(screens)} if 'read' in args else {'ok':True}
        result=dismiss_codex_trust(kind='codex',name='worker',session=None,machine=None,runner=fake,sleep=lambda _:None,authorized=True,timeout_ms=1000)
        assert result['trust_cleared']
        assert sum('send-keys' in c for c in calls)==1

    def test_name_collision_in_another_workspace_blocks(self):
        with self.assertRaises(HerdrError):
            find_live_agent(lambda _: {'agents':[{'name':'same','workspace_id':'other'}]},None,None,'same','expected')

    def test_change_cannot_escape_run_directory(self):
        for value in ['../outside','/tmp/overwrite','a/b','..']:
            with self.assertRaises(ValueError):
                expand_layout(resolve(None),change=value)

    def test_project_mapping_cannot_grant_permissions(self):
        (self.root/'mappings').mkdir()
        (self.root/'mappings/codex.json').write_text(json.dumps({'args':['--dangerously-bypass-approvals-and-sandbox']}))
        assert '--dangerously-bypass-approvals-and-sandbox' not in native_args(resolve(self.root),'orchestrator',1,'case')
        (self.root/'.herdr').mkdir()
        (self.root/'.herdr/workflow.yaml').write_text('harnesses:\n  codex:\n    args: [--dangerously-bypass-approvals-and-sandbox]\n')
        with self.assertRaises(ValueError): resolve(self.root)
        set_project(self.root,full_trust=True,auto_confirm=False)
        assert '--dangerously-bypass-approvals-and-sandbox' in native_args(resolve(self.root),'orchestrator',1,'case')

    def test_brief_and_layout_cannot_escape_even_with_full_trust(self):
        from load_config import render_brief
        from run_store import paths_for
        outside=self.root.parent/(self.root.name+'-canary')
        outside.write_text('SYNTHETIC_PRIVATE_CANARY')
        self.addCleanup(lambda:outside.unlink(missing_ok=True))
        for rel in ['../'+outside.name,str(outside)]:
            with self.assertRaises(ValueError):
                render_brief({'nodes':{'x':{'brief':rel}}},'x',project=self.root)
            with self.assertRaises(ValueError):
                paths_for(self.root,'case',{'layout':{'state':rel}})
        (self.root/'escape').symlink_to(self.root.parent,target_is_directory=True)
        with self.assertRaises(ValueError):
            paths_for(self.root,'case',{'layout':{'state':'escape/'+outside.name}})

    def test_missing_workspace_identity_blocks(self):
        with self.assertRaises(HerdrError):
            find_live_agent(lambda _: {'agents':[{'name':'same'}]},None,None,'same','expected')

    def test_predictable_temp_symlink_does_not_overwrite_outside(self):
        import run_store, init_work
        outside=self.root/'canary';outside.write_text('UNCHANGED')
        for index,writer in enumerate([run_store._write_yaml,run_store._write_json,init_work._write_yaml,init_work._write_json]):
            target=self.root/f'state{index}.yaml'
            target.with_suffix('.yaml.tmp').symlink_to(outside)
            writer(target,{'ok':True})
            assert outside.read_text()=='UNCHANGED'
            assert target.is_file() and not target.is_symlink()

    def test_corrupt_registry_does_not_grant_trust(self):
        self.registry.write_text('{bad')
        with self.assertRaises(ValueError):
            policy_for(self.root)


if __name__=='__main__':unittest.main()
