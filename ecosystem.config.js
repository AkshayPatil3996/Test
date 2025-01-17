module.exports = {   
	apps: [     {      
	name: "OpulaFrontend",       
	script: "./src/index.js",
	// Entry point of your applicationinstances: 1,          
	// Number of instancesautorestart: true,     
	// Automatically restart the app if it crasheswatch: false,          
	// Enable or disable file watchingmax_memory_restart: "500M", 
	// Restart if memory exceeds this limitenv: 
	// {         NODE_ENV: "development", }, 
	// env_production: 
	// { NODE_ENV: "production", }, 
	},
    ],

};
