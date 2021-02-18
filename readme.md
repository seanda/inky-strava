# Inky Strava

This project calls the [Strava API](http://developers.strava.com/docs/reference/#api-Activities-getLoggedInAthleteActivities) using the programmers
[Strava API Key](https://www.strava.com/settings/api) to obtain details about runs, bikes and hikes and then displays them on an [Inky wHAT](https://shop.pimoroni.com/products/inky-what?variant=21214020436051) paper/e-ink display. The graph is updated once a day and also includes the weather forecast from
DarkSky.

The idea for this project came from a [reddit mileage monitor post](https://www.reddit.com/r/RASPBERRY_PI_PROJECTS/comments/k9569y/strava_mileage_monitor_eink_pi_zero_w/)

## Hardware Set Up

There is some hardware required for this project, if you don't already have it you will need:

* A Raspberry Pi computer, I'm using a [Raspberry Pi 3b+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
* An [Inky wHAT display](https://shop.pimoroni.com/products/inky-what?variant=21214020436051), they also have a smaller version called an [Inky pHAT](https://shop.pimoroni.com/products/inky-phat?variant=12549254217811) which looks to be smaller, and more Pi Zero sized, this program wasn't written for that display so use/modify at your own risk

## Software Set Up

This project requires JavaScript, the latest version should be fine but it was written on v10.15.1. 
This project also uses python because Pimoroni Inky e-Ink display works best with Python and most of the work was layed out in python. As a note, I did attempt the npm Inky project but was unsuccessful in getting it to work.

1. Ensure your Raspberry Pi has JavaScript v10.15.1 or later
2. Ensure your RaspBerry Pi has the [Pimoroni Inky Support Libraries](https://github.com/pimoroni/inky)
3. I use [Process Manager 2](https://pm2.keymetrics.io/) to keep the Node Script running and include a pm2 process script in the repo. 
    * Use the `pm2 startup` command to get the system specific start-up script to start pm2 at start up
    * Use the `pm2 save` script at the end of the set up to make sure pm2 remembers what scripts to load on bootup.
4. Download this repository to your Pi
    * Run `npm install` to download all related components
    * Set up the authentication file in `./conf/auth.json` (details below)
    * Start the Inky-Strava process in pm2 with `pm2 start pm2_process.json`

### Setting up the Authentication file

1. Download this repository to your Raspberry Pi that you intend to use the inky wHAT display on
2. Run `npm install` to download all the components
3. Set up the authentication file in `./conf/auth.json`

the `auth.json` file should look like this:
```json
{
  "clientId": "12345",
  "clientSecret": "abcdefg12345...",
  "refreshToken": "12345abcdefg..."
}
```
The `clientId` and `clientSecret` are obtained from the [Strava API Key](https://www.strava.com/settings/api). The refresh token provided on that page only has the `activity:read` permission, which is not sufficient to get all the activities if they are marked private. In order to get a new refresh token
you can either implement OAuth2.0 or work through an article from [Josh Gotro on Medium](https://medium.com/javascript-in-plain-english/strava-api-react-app-326e63527e2c).

The key steps in this article in the event Josh takes it down are:

1. Login to your own Strava account and hit up the [Strava API Key](https://www.strava.com/settings/api) page. Note, this page won't appear unless you have an API key, so use this link to direct link ot the page.
2. Follow the instructions to create an API key. Make up a website if you don't need one and use `developers.strava.com` as the call back URL so you can use the Strava Swagger website. 
3. Navitage to the [Strava Swagger Playground](https://developers.strava.com/playground)
4. Click the **Authorize** button, enter your _clientId_ and _ClientSecret_ and then select the _activities:read_all_ box and then click the **Authorize** in the pop-up you entered all this info in.
5. A new webpage will open and ensure you check the boxes to authorize against private activities
6. Then scroll down on the Swagger page to the **Activities** controller and select the `GET` _athlete/activities_ API, and feel free to try it out to make sure the steps above have worked so far.
7. Go back to the [Strava API Key](https://www.strava.com/settings/api) and change the redirect URI to `localhost`
8.  Then we need to call the OAuth end point to request a refresh token. Paste in this URL with the particular parameters replaced with your own:
```
http://www.strava.com/oauth/authorize?client_id=54753&response_type=code
&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all
```
9. This should authorize your app again and you **should get an ERROR page**, _this is good!_
10. In the URL bar your refresh token wil be listed with the appropriate permissions: _activities:read_all_
```
http://localhost/exchange_token?state=&code=b29e1998446705436f2a2952b21eeb8f76c070c9&scope=read,activity:read_all
```
11. Add the refresh token to the auth.json file mentioned above. 🎉

## How it works

On a daily basis (9am computer time) a node-schedule job will wake the program up, it will authenticate to Strava with the refresh token to obtain an access token. Once an access token is obtained, it will call for the activities that happened after the start of the current year, or after the last time it called Strava (as not to pummel their API and get you in trouble).

On first start, the script figures out the start of the current year, and creates a new file in the `/data` directory. Then using the Strava Authentication file it calls Strava and downloads all activities from the start of the year and sorts them into Run, Ride and Hike (discarding the other activities such as walk, swim, etc). The data is then stored, along with the current time into the data file. On the next run (9am the next day) it will only query Strava for the changes since the last activity. The current year's data is stored in the `/data/data-YYYY.json` file and then it's displayed to the Inky e-Ink display.

Once a new year starts, a new file will be started and the display will start over.

The red bars progress along the bottom of each area in accordance to how close you get to the goals.

![](example/inky-strava-example.jpg?raw=true)

### Setting Goals

The goal is stored in the data file and also created by the script at the start of the year. You can change your goal in the .JSON data file throughout the year, or you can update the code for the next year to create a new goal.

## Additional Links

* [Adding Fonts](https://forums.pimoroni.com/t/inky-phat-add-fonts/5438) - This link was used to find the custom font included, along with a reference to the creator of the `ChiKarGo.ttf` font. Here is [the original source of the font](http://www.pentacom.jp/pentacom/bitfontmaker2/gallery/?id=3778 76).
* [Josh Gotro on Medium](https://medium.com/javascript-in-plain-english/strava-api-react-app-326e63527e2c) - Original post on how to get a Strava refresh token.