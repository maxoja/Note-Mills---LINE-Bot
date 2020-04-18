you need to set the following configurations to the variables of the environment you will run this application on

USER_ID = '<LINE dev console> / <your chhannel> / <basic settings>'
CHANNEL_ACCESS_TOKEN = '<LINE dev console> / <your channel> / <messging API>'
EVERNOTE_SANDBOX_ACCESS_TOKEN = '<please check https://dev.evernote.com/doc/articles/dev_tokens.php>'

to set Heroku env var (either programmatically or by using dashboard)
https://devcenter.heroku.com/articles/config-vars

to set Windows env var
`setx USER_ID <your LINE user id>`
`setx CHANNEL_ACCESS_TOKEN <your LINE channel access token>`
`setx CHANNEL_SECRET <your LINE channel secret>`
`setx EVERNOTE_SANDBOX_ACCESS_TOKEN <your sandbox evernote access token>`