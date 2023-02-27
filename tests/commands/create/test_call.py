import pytest

from briefcase.commands.create import git
from briefcase.exceptions import BriefcaseCommandError


def test_no_git(tracking_create_command, monkeypatch):
    """If Git is not installed, an error is raised."""

    def monkeypatch_verify_git(*a, **kw):
        raise BriefcaseCommandError("Briefcase requires git, but it is not installed")

    monkeypatch.setattr(git, "verify_git_is_installed", monkeypatch_verify_git)

    # The command will fail tool verification.
    with pytest.raises(
        BriefcaseCommandError,
        match=r"Briefcase requires git, but it is not installed",
    ):
        tracking_create_command()


def test_create(tracking_create_command, tmp_path):
    """The create command can be called."""
    tracking_create_command()

    # The right sequence of things will be done
    assert tracking_create_command.actions == [
        # Host OS is verified
        ("verify-host",),
        # Tools are verified
        ("verify-tools",),
        # Create the first app
        ("generate", tracking_create_command.apps["first"]),
        ("support", tracking_create_command.apps["first"]),
        ("verify-app-tools", tracking_create_command.apps["first"]),
        ("code", tracking_create_command.apps["first"], False),
        ("requirements", tracking_create_command.apps["first"], False),
        ("resources", tracking_create_command.apps["first"]),
        ("cleanup", tracking_create_command.apps["first"]),
        # Create the second app
        ("generate", tracking_create_command.apps["second"]),
        ("support", tracking_create_command.apps["second"]),
        ("verify-app-tools", tracking_create_command.apps["second"]),
        ("code", tracking_create_command.apps["second"], False),
        ("requirements", tracking_create_command.apps["second"], False),
        ("resources", tracking_create_command.apps["second"]),
        ("cleanup", tracking_create_command.apps["second"]),
    ]

    # New app content has been created
    assert (
        tmp_path / "base_path" / "build" / "first_0.0.1" / "tester" / "dummy" / "new"
    ).exists()
    assert (
        tmp_path / "base_path" / "build" / "second_0.0.2" / "tester" / "dummy" / "new"
    ).exists()


def test_create_single(tracking_create_command, tmp_path):
    """The create command can be called to create a single app from the config."""
    tracking_create_command(app=tracking_create_command.apps["first"])

    # The right sequence of things will be done
    assert tracking_create_command.actions == [
        # Host OS is verified
        ("verify-host",),
        # Tools are verified
        ("verify-tools",),
        # Create the first app
        ("generate", tracking_create_command.apps["first"]),
        ("support", tracking_create_command.apps["first"]),
        ("verify-app-tools", tracking_create_command.apps["first"]),
        ("code", tracking_create_command.apps["first"], False),
        ("requirements", tracking_create_command.apps["first"], False),
        ("resources", tracking_create_command.apps["first"]),
        ("cleanup", tracking_create_command.apps["first"]),
    ]

    # New app content has been created
    assert (
        tmp_path / "base_path" / "build" / "first_0.0.1" / "tester" / "dummy" / "new"
    ).exists()
    assert not (
        tmp_path / "base_path" / "build" / "second_0.0.2" / "tester" / "dummy" / "new"
    ).exists()
