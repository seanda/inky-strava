'use strict'
const axios = require('axios')
const fs = require('fs')
const schedule = require('node-schedule')
const { exec } = require ('child_process')
const auth = require('./conf/auth.json')
const yargs = require('yargs').argv


const strava = axios.create({
  baseURL: 'https://www.strava.com/api/v3'
})

// Read in existing data
const year = new Date().getFullYear()
const dataFile = `./data/data-${year}.json`
let yearData
if (fs.existsSync(dataFile)) {
  yearData = JSON.parse(fs.readFileSync(dataFile))
} else {
  if (!fs.existsSync('./data')) {
    fs.mkdirSync('./data');
  }
  yearData = createYear()
}

if (yargs.now) {
  getStravaData()
} else {
  console.log(`[${new Date().toISOString()}] Program Started - Next update at 9:00am`)
  schedule.scheduleJob('0 0 09 * * *', () => {
    getStravaData()
  })
}

async function getStravaData() {
  let accessToken

  // Use Refresh Token to get Access Token
  let authError = false
  await strava.post(`/oauth/token?client_id=${auth.clientId}&client_secret=${auth.clientSecret}&refresh_token=${auth.refreshToken}&grant_type=refresh_token`)
  .then((response) => {
    if (response.status == 200) {
      accessToken = response.data.access_token
      console.log(`[${new Date().toISOString()}] Authenticated to Strava & Updating`)
    }
  })
  .catch((err) => {
    console.log(`[${new Date().toISOString()}] ERR: Failed to authenticate with Strava: ${err.response.status} - ${err.response.statusText}`)
    authError = true
  })

  // Use Access Token to get Data since last call
  if (!authError) {
    await strava.get(`/athlete/activities?access_token=${accessToken}&after=${yearData.conf.lastEpoch}`)
    .then((response) => {

      // Process Data
      let latestActivityDate
      let allActivities = response.data
      console.log(`[${new Date().toISOString()}] Downloaded ${allActivities.length} activites from Strava`)

      for (let i = 0; i < allActivities.length; i++) {
        latestActivityDate = new Date(allActivities[i].start_date)
        if (allActivities[i].type == 'Run') {
          yearData.run.distance += allActivities[i].distance / 1000
          yearData.run.elevation += allActivities[i].total_elevation_gain / 1000
          yearData.run.totalTime += allActivities[i].moving_time /60 /60
          yearData.run.activities += 1
        } else if (allActivities[i].type == "Ride") {
          yearData.bike.distance += allActivities[i].distance / 1000
          yearData.bike.elevation += allActivities[i].total_elevation_gain / 1000
          yearData.bike.totalTime += allActivities[i].moving_time /60 /60
          yearData.bike.activities += 1
        } else if (allActivities[i].type = "Hike") {
          yearData.hike.distance += allActivities[i].distance / 1000
          yearData.hike.elevation += allActivities[i].total_elevation_gain / 1000
          yearData.hike.totalTime += allActivities[i].moving_time /60 /60
          yearData.hike.activities += 1
        }
      }

      // Save new data back to the storage file
      if (allActivities.length > 0) {
        yearData.conf.lastEpoch = Math.round(latestActivityDate / 1000)
        console.log(`latest Activity Date: ${yearData.conf.lastEpoch} | current time: ${Math.round(new Date() / 1000)}`)
      }
      fs.writeFileSync(dataFile, JSON.stringify(yearData))
      if (yargs.now) {
        console.log(yearData)
      }

      // Send to the screen
      console.log(`[${new Date().toISOString()}] Updating Inky wHAT`)
      exec(`./strava-vision.py --rund=${yearData.run.distance.toFixed(1)} --rune=${yearData.run.elevation.toFixed(2)} --runc=${yearData.run.activities} --runp=${((yearData.run.distance/yearData.run.runGoal) * 100).toFixed(0)} --biked=${yearData.bike.distance.toFixed(1)} --bikee=${yearData.bike.elevation.toFixed(2)} --bikec=${yearData.bike.activities} --bikep=${((yearData.bike.distance/yearData.bike.bikeGoal) * 100).toFixed(0)} --hiked=${yearData.hike.distance.toFixed(1)} --hikee=${yearData.hike.elevation.toFixed(2)} --hikec=${yearData.hike.activities} --hikep=${((yearData.hike.distance/yearData.hike.hikeGoal) * 100).toFixed(0)}`
        , (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
      });

    })
    .catch((err) => {
      console.log(`[${new Date().toISOString()}] Error downloading activities from Strava:  ${err.response.status} - ${err.response.statusText}`)
    })
  }
}

function createYear() {
  //Get Start of Year in Epoch time
  let startOfYear = new Date()
  startOfYear.setMonth(0)
  startOfYear.setDate(1)
  startOfYear.setHours(1)
  startOfYear.setMinutes(0)
  startOfYear.setSeconds(0)
  const epochStartOfYear = Math.round(startOfYear / 1000)

  let yearData = {}

  yearData.run = {}
  yearData.run.distance = 0
  yearData.run.elevation = 0
  yearData.run.activities = 0
  yearData.run.totalTime = 0
  yearData.run.runGoal = 1000 // set  goal to 1000 km
  
  yearData.bike = {}
  yearData.bike.distance = 0
  yearData.bike.elevation = 0
  yearData.bike.activities = 0
  yearData.bike.totalTime = 0
  yearData.bike.bikeGoal = 500 // set goal to 500 km

  yearData.hike = {}
  yearData.hike.distance = 0
  yearData.hike.elevation = 0
  yearData.hike.activities = 0
  yearData.hike.totalTime = 0
  yearData.hike.hikeGoal = 150 // set goal to 150 km

  yearData.conf = {}
  yearData.conf.lastEpoch = epochStartOfYear

  return yearData
}