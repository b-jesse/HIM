;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; ------------------------------------------------- Main --------------------------------------------------- ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; ----------------------------------------------- Extensions ----------------------------------------------- ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;´
extensions [
  csv
  table
  profiler
]

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; ------------------------------------------------ Inlcude ------------------------------------------------- ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;´
__includes [
  "class.nls"
  "setup.nls"
  "func.nls"
  "write.nls"
  "plot.nls"
]

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; ------------------------------------------------ Globals ------------------------------------------------- ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
globals [
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; Meta data
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  meta.name
  meta.date
  meta.version
  meta.run
  meta.run_no
  meta.run_path
  meta.config

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; Settings
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  settings.debug
  settings.track
  settings.plot
  settings.write
  settings.seperator

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; Scenario
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  scenario.ref
  scenario.co2_tax
  scenario.h2_subsidy
  scenario.h2_guarant
  scenario.res_subsidy
  scenario.power_subsidy
  scenario.power_guarant
  scenario.elc_subsidy
  scenario.elc_guarant
  scenario.man_subsidy
  scenario.time_lag

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; Globals
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ; Global
  global.year

  ; Power market
  global.PM.no_pp
  global.PM.no_res
  global.PM.no_investment
  global.PM.installed_capacity
  global.PM.cumulative_capacity
  global.PM.added_capacity
  global.PM.threshold_min
  global.PM.roi_target
  global.PM.lcoe
  global.PM.weighted_price
  global.PM.cost_share
  global.PM.time_wo_agent
  global.PM.list_demand
  global.PM.list_util
  global.PM.list_production
  global.PM.list_price
  global.PM.list_payout
  global.PM.list_shares

  ; Hydrogen market
  global.HM.no_hp
  global.HM.no_elc
  global.HM.no_investment
  global.HM.price_h2
  global.HM.payout_h2
  global.HM.production_h2
  global.HM.lcoh
  global.HM.installed_capacity
  global.HM.cumulative_capacity
  global.HM.added_capacity
  global.HM.threshold_min
  global.HM.roi_target
  global.HM.time_wo_agent
  global.HM.list_util
  global.HM.list_production
  global.HM.list_income
  global.HM.list_expense

  ; Electrolyzer market
  global.EM.no_ep
  global.EM.no_man
  global.EM.no_investment
  global.EM.cost_elc
  global.EM.installed_capacity
  global.EM.cumulative_capacity
  global.EM.added_capacity
  global.EM.threshold_min
  global.EM.roi_target
  global.EM.lcoe
  global.EM.time_wo_agent

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; Constants
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ; Global
  const.discount_rate
  const.eta_gas_turbine
  const.eta_electrolyzer
  const.eta_steam_reforming

  ; Carbon intensity
  const.gas_co2
  const.coal_co2
  const.oil_co2

  ; Function adjustment parameters
  const.alpha
  const.beta
  const.gamma
  const.delta
  const.epsilon

  ; Power market
  const.PM.delta_threshold
  const.PM.investment_time
  const.PM.p_elc_min
  const.RES.lifetime
  const.RES.lifetime_range
  const.RES.new_capacity
  const.RES.max_capacity
  const.RES.max_capacity_rate

  ; Hydrogen market
  const.HM.delta_threshold
  const.HM.investment_time
  const.ELC.lifetime
  const.ELC.lifetime_range
  const.ELC.target_capacity
  const.ELC.new_capacity

  ; Electrolyzer market
  const.EM.delta_threshold
  const.EM.investment_time
  const.EM.inexperience_penalty_max
  const.EM.global_share
  const.MAN.lifetime
  const.MAN.lifetime_range
  const.MAN.target_capacity
  const.MAN.new_capacity
  const.MAN.learning_rate

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; Start values
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ; Power market
  init.PM.no_pp_0
  init.PM.no_res_0
  init.PM.c_gas_0
  init.PM.c_coal_0
  init.PM.c_oil_0
  init.PM.c_res_0

  ; Hydrogen market
  init.HM.no_hp_0
  init.HM.no_elc_0
  init.HM.threshold_0
  init.HM.c_elc_0

  ; Electrolyzer market
  init.EM.no_ep_0
  init.EM.no_man_0
  init.EM.threshold_0
  init.EM.c_man_0
  init.EM.global_cap_0

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; Files
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  infile.PM.ts_demand_daily
  infile.PM.ts_demand_yearly
  infile.PM.ts_co2_yearly
  infile.HM.h2_demand

  outfile.PM.year
  outfile.PM.day
  outfile.PP.year
  outfile.RES.year
  outfile.HM.year
  outfile.HM.day
  outfile.HP.year
  outfile.ELC.year
  outfile.EM.year
  outfile.EP.year
  outfile.MAN.year
  outfile.SALE.year
  outfile.CONFIG

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; Governmental actions
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  GOV.h2_subsidy ;; extra percentage on the current hydrogen price [%]
  GOV.h2_guarant ;; guaranteed price which is payed at least [€/MWh]
  GOV.res_subsidy ;; percentage of the renewables investment cost covered by the GOV [%]
  GOV.power_subsidy ;; extra percentage on the current electricity price [%]
  GOV.power_guarant ;; guaranteed price which is payed at least [€/MWh]
  GOV.elc_subsidy ;; percentage of the electrolyzer investment costs covered by the GOV [%]
  GOV.elc_guarant ;; guaranteed price for electrolyzer [€/MW]
  GOV.man_subsidy ;; percentage of the manufacturing cap investment costs covered by the GOV [%]

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; Tracking values
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ; Power market
  track.PM.no_pp
  track.PM.no_res
  track.PM.no_investment
  track.PM.installed_capacity
  track.PM.cumulative_capacity
  track.PM.added_capacity
  track.PM.threshold_min
  track.PM.lcoe
  track.PM.weighted_price
  track.PM.cost_share
  track.PM.time_wo_agent
  track.PM.list_demand
  track.PM.list_util
  track.PM.list_production
  track.PM.list_price
  track.PM.list_payout
  track.PM.list_shares

  ; Hydrogen market
  track.HM.no_hp
  track.HM.no_elc
  track.HM.no_investment
  track.HM.installed_capacity
  track.HM.cumulative_capacity
  track.HM.added_capacity
  track.HM.threshold_min
  track.HM.lcoh
  track.HM.price_h2
  track.HM.payout_h2
  track.HM.demand_h2
  track.HM.time_wo_agent
  track.HM.list_util
  track.HM.list_production
  track.HM.list_income
  track.HM.list_expense

  ; Electrolyzer market
  track.EM.no_ep
  track.EM.no_man
  track.EM.no_investment
  track.EM.cost_elc
  track.EM.installed_capacity
  track.EM.cumulative_capacity
  track.EM.added_capacity
  track.EM.threshold_min
  track.EM.lcoe
  track.EM.time_wo_agent
]

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; ------------------------------------------------- Setup -------------------------------------------------- ;
; Order of setup is:                                                                                         ;
; 1. setup-meta - setting all meta.values (done in main.nlogo)                                               ;
; 2. setup - setting everything else                                                                         ;
; 2.1 setup-settings - setting the settings for the current run                                              ;
; 2.2 setup-scenario - setting all boolean for the current scenario                                          ;
; 2.3 setup-files - setting up all files                                                                     ;
; 2.3.1 setup-input - setting all input files                                                                ;
; 2.3.2. setup-output - setting up all output files (optional)                                               ;
; 2.4 setup-constants - setting all constant values (optional: use sensitivity values)                       ;
; 2.5 setup-init - setting all start values (optional: use sensitivity values)                               ;
; 2.6 setup-world - setting up the model world (optinal: use sensitivity values)                             ;
; 2.6.1 setup-government - setting the subsidy values (optional: use sensitivity values)                     ;
; 2.6.2 setup-pm - setting up the power market                                                               ;
; 2.6.2.1 setup-res - setting up the renewables                                                              ;
; 2.6.2.2 setup-pp - seeting up the power producers                                                          ;
; 2.6.3 setup-hm - setting up the hydrogen market                                                            ;
; 2.6.3.1 setup-elc - setting up the electrolyzers                                                           ;
; 2.6.3.2 setup-hp - setting up the hydrogen producers                                                       ;
; 2.6.4 setup-em - setting up the electrolyzer market                                                        ;
; 2.6.4.1 setup-man - setting up the manufacturing capacities                                                ;
; 2.6.4.2 setup-ep - setting up the electrolyzer producers                                                   ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
to setup-meta
  clear-all
  clear-all-plots
  file-close-all
  reset-ticks

  ;; Set meta data
  set meta.name "Bernhard Jesse"
  set meta.date func.get_date
  set meta.version 1.5
  set meta.run ""
  set meta.run_no 0
  set meta.run_path ""
  set meta.config ""

  ;; DEBUG ONLY PLEASE DELETE ME FOR MORE runs
  ;;random-seed 123456

end

to setup
  ;; Setup settings
  setup-settings
  ;; Setup scenario
  setup-scenario
  ;; Setup all files
  setup-files
  ;; Setup all constant values
  setup-constants
  ;; Setup all starting values
  setup-init
  ;; Setup the world
  setup-world

end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; -------------------------------------------------- Go ---------------------------------------------------- ;
; Order of the model each year is:                                                                           ;
; 1. Check if run should end                                                                                 ;
; 2. Set the hydrogen price for the current year                                                             ;
; 2.1 Determine the amount of hydrogen produced                                                              ;
; 2.2 Get hydrogen price based on supply                                                                     ;
; 3. Daily actions                                                                                           ;
; 3.1 Power Market daily actions                                                                             ;
; 3.2 Hydrogen Market daily actions                                                                          ;
; 4. Yearly actions                                                                                          ;
; 4.1 Power Market yearly actions                                                                            ;
; 4.2 Hydrogen Market yearly actions                                                                         ;
; 4.3 Electrolyzer Market yearly actions                                                                     ;
; 5. Next year                                                                                               ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
to go
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; 1. Check if run should end
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  let tmp.year_end 80
  (ifelse
    global.year = tmp.year_end [
      ;; Write data
      if settings.write [
        write.CONFIG
        file-close-all
      ]
      print word word "Run " meta.run_no " complete!"
      stop
    ]
    global.year > tmp.year_end [
      print "WARNING: CURRENT YEAR EXCEEDS MAXIMUM YEAR. MODEL STOPS NOW!"
      stop
    ]
  )

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; 2. Set the hydrogen price for the current year
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  func.hm.set_h2_price

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; 3. Daily actions
  ;; 3.1 Power market daily actions
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  func.pm.daily

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; 3.2 Hydrogen Market daily actions
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  func.hm.daily

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; 4. Yearly actions
  ;; 4.1 Power market yearly actions
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  func.pm.yearly

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; 4.2 Hydrogen Market yearly actions
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  func.hm.yearly

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; 4.3 Electrolyzer Market yearly actions
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  func.em.yearly

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;; 5. Next year
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  set global.year (global.year + 1)
  tick
end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; ------------------------------------------------- Profiler ----------------------------------------------- ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
to profiler
  setup
  profiler:start         ;; start profiling
  repeat 20 [ go ]       ;; run something you want to measure
  profiler:stop          ;; stop profiling
  print profiler:report  ;; view the results
  profiler:reset         ;; clear the data
end
@#$#@#$#@
GRAPHICS-WINDOW
210
10
628
429
-1
-1
10.0
1
10
1
1
1
0
1
1
1
-20
20
-20
20
0
0
1
ticks
30.0

BUTTON
6
11
72
44
setup
setup-meta\nsetup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
75
10
138
43
NIL
go
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
142
10
205
43
NIL
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

MONITOR
6
48
63
93
year
global.year
17
1
11

PLOT
6
97
206
247
PM Generation
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"pen-res_max" 1.0 0 -16777216 true "" ""
"pen-demand_total" 1.0 0 -7500403 true "" ""
"pen-demand_other" 1.0 0 -2674135 true "" ""
"pen-res" 1.0 0 -955883 true "" ""
"pen-demand" 1.0 0 -6459832 true "" ""

PLOT
6
250
206
400
PM Cost
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"pen-res" 1.0 0 -16777216 true "" ""
"pen-hydrogen" 1.0 0 -7500403 true "" ""
"pen-res_p" 1.0 0 -2674135 true "" ""
"pen-hydrogen_p" 1.0 0 -14070903 true "" ""

PLOT
7
404
207
554
PM Installed capacities
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"pen-res" 1.0 0 -16777216 true "" ""

PLOT
7
558
207
708
PM Share
NIL
NIL
0.0
1.0
0.0
1.0
true
false
"" ""
PENS
"pen-res" 1.0 0 -16777216 true "" ""

PLOT
211
431
411
581
HM Installed capacities
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"pen-elc" 1.0 0 -16777216 true "" ""
"pen-man" 1.0 0 -7500403 true "" ""

PLOT
211
583
411
733
Agents
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"pen-pp" 1.0 0 -7500403 true "" ""
"pen-hp" 1.0 0 -14730904 true "" ""
"pen-ep" 1.0 0 -15040220 true "" ""

PLOT
210
737
410
887
HM Utilization
NIL
NIL
0.0
10.0
0.0
1.0
true
false
"" ""
PENS
"pen-elc" 1.0 0 -16777216 true "" ""

PLOT
414
583
614
733
Investments
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"pen-pp" 1.0 0 -7500403 true "" ""
"pen-hp" 1.0 0 -15582384 true "" ""
"pen-ep" 1.0 0 -15575016 true "" ""

PLOT
414
431
614
581
HM Produced
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"pen-h2" 1.0 0 -16777216 true "" ""

PLOT
414
738
614
888
EM Cost
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"pen-cost" 1.0 0 -7500403 true "" ""
"pen-cost_act" 1.0 0 -2674135 true "" ""

@#$#@#$#@
## WHAT IS IT?

(a general understanding of what the model is trying to show or explain)

## HOW IT WORKS

(what rules the agents use to create the overall behavior of the model)

## HOW TO USE IT

(how to use the model, including a description of each of the items in the Interface tab)

## THINGS TO NOTICE

(suggested things for the user to notice while running the model)

## THINGS TO TRY

(suggested things for the user to try to do (move sliders, switches, etc.) with the model)

## EXTENDING THE MODEL

(suggested things to add or change in the Code tab to make the model more complicated, detailed, accurate, etc.)

## NETLOGO FEATURES

(interesting or unusual features of NetLogo that the model uses, particularly in the Code tab; or where workarounds were needed for missing features)

## RELATED MODELS

(models in the NetLogo Models Library and elsewhere which are of related interest)

## CREDITS AND REFERENCES

(a reference to the model's URL on the web if it has one, as well as any other necessary credits, citations, and links)
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.4.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
