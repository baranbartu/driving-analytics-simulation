'use strict';

const Router = require('express');
const producer = require('../events/producer');

const LOCATIONS_TOPIC = process.env.LOCATIONS_TOPIC;
const DRIVING_ANALYTICS_TOPIC = process.env.DRIVING_ANALYTICS_TOPIC;


const getEventApiRoutes = (app) => {
  const router = new Router();

  router.post('/location', (req, res) => {
    const locationData = req.body;
    console.log('location data received: ', locationData);
    producer.send(locationData, LOCATIONS_TOPIC);
    res.send(locationData);
  });

  router.post('/driving-analytics', (req, res) => {
    const drivingAnalyticsData = req.body;
    console.log('driving analytics data received: ', drivingAnalyticsData);
    producer.send(drivingAnalyticsData, DRIVING_ANALYTICS_TOPIC);
    res.send(drivingAnalyticsData);
  });

  app.use('/api/v1/event', router);
};

module.exports = getEventApiRoutes;
