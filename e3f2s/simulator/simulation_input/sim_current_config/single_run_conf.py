sim_scenario_conf = {

	"requests_rate_factor": 1,
	"n_vehicles_factor": 1,

	"time_estimation": True,
	"queuing": True,

	"alpha": 26,
	"beta": 100,
	"n_poles_n_vehicles_factor": 0.25,

	"hub": False,
	"hub_zone_policy": "",

	"distributed_cps": True,
	"system_cps": True,
	"cps_placement_policy": "num_parkings",
	"cps_zones_percentage": 0.05,

	"battery_swap": False,
	"avg_reach_time": 20,
	"avg_service_time": 1,

	"n_workers": 1000,
	"relocation": False,

	"user_contribution": False,
	"willingness": 0,

}
