# Miscellaneous features

Here's where extra features are documented

## Wentlive emails

It's possible to have snap send out emails saying the project was snapped automatically after every
snap. These can be enabled for all projects in `config.py`, or on a per project basis using the
`wentlive` command in a `manifest.py`. There is also a `no_wentlive` command if a project specifically
does not want to send a wentlive email.

Check `config.py` if you need to specify an external smtp service to use for sending email.

## Tagging

Snap can be configured to `git tag` projects when they're snapped. Like wentlive emails these can
be enabled globally in `config.py` or on a per-project basis using the `tag` command in
`manifest.py`.

Note that to tag a project the user running snap must have push permissions on the repository in
question.

## *.nosnap

Snap will automatically look for files with the `.nosnap` extension in the root of the project. If it
finds one it will not continue with the snap, and instead will dump the contents of the file to output
and send the user back to the main menu.
