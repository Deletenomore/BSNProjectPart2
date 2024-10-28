// next.config.js
const path = require("path");

module.exports = {
  webpack: (config, { dev, isServer }) => {
    if (dev) {
      config.cache = false; // Disable caching during development
    }
    return config;
  },
};
