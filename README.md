# Airport Aircraft Data: DOH_2014, HKG_2017, & PEK_2014
* [Copyright]: Intelligent Systems Engineering (ISE) research team at Queen Mary, University of London. https://www.qmul.ac.uk/intelligentsystems/
* [Notes]:     Shared open-source data is for academic purposes only and should not be used for commercial activities or other events that may have adverse effects on the public interest.

Welcome to discuss and collaborate! Edited by Songwei Liu (https://orcid.org/0000-0002-9892-0918) in August 2025.

Thank you for your attention and interests in constructing airport taxiway networks as multigraphs via taking speed profiles into account.


####### Overall Introduction #######

This folder includes taxiway layouts of Doha International Airport (DOH), Hongkong International Airport (HKG), and Beijing Capital International Airport (PEK). The layout data was obtained via https://www.openstreetmap.org. Within each airport layout, taxiways are divided into diverse-distance segments to facilitate the generation and assignment of speed profiles. There are two types of taxiway segments, namely straight and turning, where the difference is that a turning segment and its predecerssor segment (in the direction of aircraft taxiing) have an angle not less than 30 degrees. The reason for distinguishing straight and turning segments is that higher costs are usually incurred during turning than taxiing straightly.

Speed profiles define the taxiing speed along time and are generated using the method in [1]. As aircraft weight categories affect movement parameters and hence speed profile generations, speed profiles for different weight categories are generated separately. 10 speed profiles that hold nondominated objective values are assigned for every taxiway segment. Optimisation objectives are to minimise taxi time, fuel consumption, and pollution emission.

Each straight segment is categorised as breakaway, intermediate and holding. The start/end speed is fixed to 5.14 m/s (10 knots), except for breakaway and holding segments where the start and end speeds are 0, respectively. Regarding each straight segment, its speed profiles always include four phases including acceleration, constant speed, deceleration and rapid deceleration, as illustrated in Fig.3 of [2].

Turning segment has a constant speed 5.14 m/s.

To match the routing and scheduling task of taxiing aircraft with real-world scenarios, real-life operation instances in the three airports are adopted. Each operation instance dataset contains landing/pushback time, gate/runway exit, and aircraft weight category for each flight, within a specific period in the past. Flight instances were obtained via https://www.FlightRadar24.com:
   * DOH: 16 March 2014 from 17:00 to 23:00
   * HKG: 17 January 2017 from 0:00 to 24:00
   * PEK: 9 July 2014 from 9:00 to 14:00
   * Download datasets via https://www.dropbox.com/scl/fi/1eojq7fce2kyoyrx68axy/main_data.zip?rlkey=ibp6o7b7c8pvtzjj0o57svjoa&st=9ztwi5rv&dl=0. After decompressing the downloaded file, paste the file folder to the same path where other Python files are stored in your PC.

For detailed statistics on these three instance datasets, refer to Table 3 in [3].
During the above three periods, three airports only had operating aircraft in medium and heavy categories, and it is why the light weight category is not considered when generating speed profiles.

####### Construction of Airport Layout and Import Flight Data  #######

Use functions 'read_in_airport_data(airportInstance)' and 'initialise_layout_graph(airport_edges)' in 'ReadAirportAircraftData.py'

Relationship between the two functions:
   * airport_nodes, airport_edges, dbases, conflicting_edges, aircrafts = read_in_airport_data(airportInstance)
     * 'airportInstance' is a user defined input indicating which airport is gonna used, 'doh', 'hkg', or 'pek'
   * G_layout = initialise_layout_graph(airport_edges)


####### Assignment of Speed Profiles to Airport Layout #######

Use function 'read_in_graph(G_layout,segment_dict,airport_edges,airport_nodes,edge_successors,dbases,speed_profiles,airportInstance)' in 'airport_functions.py'

The input 'speed_profiles' is defined by user, indicating how many speed profiles are used for routing, where the maximum is 10.

Output of the function 'read_in_graph()': G_seg_base_H_all, ma_H, G_seg_base_M_all, ma_M
   * G_seg_base_H_all: the complete set of graph segments modelled for heavy aircraft.
   * ma_H: the maximum objective value (single-value cost) across multiple objectives among all speed profiles for heavy aircraft.
   * G_seg_base_M_all: the complete set of graph segments modelled for medium aircraft.
   * ma_M: the maximum objective value (single-value cost) across multiple objectives among all speed profiles for medium aircraft.


####### Description of Data Structures #######

Within files whose names begin with 'dbase_', speed profiles are stored.

Regarding data in 'dbase_' files:
   * Each line has 11 columns.
   * Column  1 : Taxiway segment length in meters, to map with taxiways in layout via length.
   * Column  2 - 11: Values regarding Objective 1 (taxi time) for the 10 speed profiles, respectively.
   * Column 12 - 21: Values regarding Objective 2 (fuel consumption) for the 10 speed profiles, respectively.
   * Column 22 - 31: Values regarding Objective 3 (pollution emission) for the 10 speed profiles, respectively.
   * Column 32 - 41: Acceleration rate 1 (a1) for the 10 speed profiles, respectively.
   * Column 42 - 51: Distance 1 (d1) for the 10 speed profiles, respectively.
   * Column 52 - 61: Distance 2 (d2) for the 10 speed profiles, respectively.
   * Column 62 - 71: NOT USED IN FILES OR FUNCTIONS.
   * Column 72 - 81: Distance 3 (d3) for the 10 speed profiles, respectively.
   * Column 82 - 91: Acceleration rate 2 (a2) for the 10 speed profiles, respectively.
   * Column 92 - 101:NOT USED IN FILES OR FUNCTIONS.

Regarding detailed descriptions of a1, d1, d2, d3, and d4, refer to Fig.3 in [2]. The 'a3' in Fig.3 of [2] is set to 0.98, as demonstrated in 'database.py'.


References

[1] M. Weiszer, J. Chen, and P. Stewart, ‘A real-time active routing approach via a database for airport surface movement’, Transportation Research Part C: Emerging Technologies, vol. 58, pp. 127–145, 2015.

[2] J. Chen, M. Weiszer, P. Stewart, et al., ‘Toward a more realistic, cost-Effective, and greener ground movement through active routing—part i: Optimal speed profile generation’, IEEE Transactions on Intelligent Transportation Systems, vol. 17, no. 5, pp. 1196-1209, 2016.

[3] M. Weiszer, E. K. Burke, J. Chen, ‘Multi-objective routing and scheduling for airport ground movement’, Transportation Research Part C: Emerging Technologies, 119, 102734, 2020.
