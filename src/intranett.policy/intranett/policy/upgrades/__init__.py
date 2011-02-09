from Acquisition import aq_get

from Products.GenericSetup.upgrade import _registerUpgradeStep
from Products.GenericSetup.upgrade import UpgradeStep

from intranett.policy.config import BASE_PROFILE
from intranett.policy.config import POLICY_PROFILE
from intranett.policy.config import THEME_PROFILE

UPGRADES = []


def upgrade_to(dest):

    def decorator(fun):
        UPGRADES.append((dest, fun))

        def replacement(context):
            return fun(context)

        return replacement
    return decorator


def register_upgrades():
    from intranett.policy.upgrades import steps
    steps # pyflakes, register steps during import
    for dest, handler in UPGRADES:
        step = UpgradeStep(u'Upgrade %s' % handler.__name__,
            u'intranett.policy:default', str(dest - 1), str(dest), None,
            handler, checker=None, sortkey=0)
        _registerUpgradeStep(step)


def null_upgrade_step(tool):
    """This is a null upgrade, use it when nothing happens."""
    pass # pragma: no cover


def run_upgrade(setup, profile_id=POLICY_PROFILE):
    request = aq_get(setup, 'REQUEST')
    request['profile_id'] = profile_id

    upgrades = setup.listUpgrades(profile_id)

    steps = []
    for u in upgrades:
        if isinstance(u, list): # pragma: no cover
            steps.extend([s['id'] for s in u])
        else:
            steps.append(u['id'])

    request.form['upgrades'] = steps
    setup.manage_doUpgrades(request=request)


def run_all_upgrades(setup):
    run_upgrade(setup, BASE_PROFILE)
    run_upgrade(setup, THEME_PROFILE)
    run_upgrade(setup)

    base_updated = compare_profile_versions(setup, BASE_PROFILE)
    theme_updated = compare_profile_versions(setup, THEME_PROFILE)
    policy_updated = compare_profile_versions(setup, POLICY_PROFILE)
    return all([base_updated, theme_updated, policy_updated])


def compare_profile_versions(setup, profile_id):
    current = setup.getVersionForProfile(profile_id)
    current = tuple(current.split('.'))
    last = setup.getLastVersionForProfile(profile_id)
    return current == last
