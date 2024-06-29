// Queries:
// Match (s:Saison {jahr:2018})--(:Staffel {ak:10})-[r]-(v:Verein) where r.kampflos>0 return r,v.name order by r.kampflos desc

MERGE (saison2018:Saison { name:"Saison 2018/2019", jahr:2018, url:'https://svs.portal64.de/ergebnisse/show/2018/1' })
MERGE (s2018ddu20:Staffel {name:"Bezirksliga Dresden U20", url:'https://svs.portal64.de/ergebnisse/show/2018/1535', region:"Dresden", ak:20, partien:40, kampflos:9})
MERGE (s2018slu20:Staffel {name:"1. Sachsenjugendliga U20", url:'https://svs.portal64.de/ergebnisse/show/2018/1635', region:"Sachsen", ak:20, partien:(112+36), kampflos:15})
MERGE (s2018slu20z:Staffel {name:"2. Sachsenjugendliga U20", url:'https://svs.portal64.de/ergebnisse/show/2018/1633', region:"Sachsen", ak:20, partien:48, kampflos:2})
MERGE (s2018slu16:Staffel {name:"Sachsenliga U16", url:'https://svs.portal64.de/ergebnisse/show/2018/1631', region:"Sachsen", ak:16, partien:180, kampflos:2})
MERGE (s2018ddu16:Staffel {name:"Bezirksliga Dresden U16", url:'https://svs.portal64.de/ergebnisse/show/2018/1537', region:"Dresden", ak:16, partien:80, kampflos:2})
MERGE (s2018ddu16ka:Staffel {name:"Bezirksklasse Dresden U16 St. A", url:'https://svs.portal64.de/ergebnisse/show/2018/1545', region:"Dresden", ak:16, partien:96, kampflos:10})
MERGE (s2018ddu16kb:Staffel {name:"Bezirksklasse Dresden U16 St. B", url:'https://svs.portal64.de/ergebnisse/show/2018/1547', region:"Dresden", ak:16, partien:120, kampflos:10})
MERGE (s2018ddu14:Staffel {name:"Bezirksliga Dresden U14", url:'https://svs.portal64.de/ergebnisse/show/2018/1541', region:"Dresden", ak:14, partien:96, kampflos:17}) // checked
MERGE (s2018ddu14k:Staffel {name:"Bezirksklasse Dresden U14", url:'https://svs.portal64.de/ergebnisse/show/2018/1549', region:"Dresden", ak:14, partien:168, kampflos:12})
MERGE (s2018ddu12:Staffel {name:"Bezirksliga Dresden U12", url:'https://svs.portal64.de/ergebnisse/show/2018/1543', region:"Dresden", ak:12, partien:224, kampflos:0})
MERGE (s2018ddu12ka:Staffel {name:"Bezirksklasse Dresden U12 St. A", url:'https://svs.portal64.de/ergebnisse/show/2018/1551', region:"Dresden", ak:12, partien:168, kampflos:2})
MERGE (s2018ddu12kb:Staffel {name:"Bezirksklasse Dresden U12 St. B", url:'https://svs.portal64.de/ergebnisse/show/2018/1553', region:"Dresden", ak:12, partien:168, kampflos:23})
MERGE (s2018ddu10:Staffel {name:"Bezirksliga Dresden U10", url:'https://svs.portal64.de/ergebnisse/show/2018/1643', region:"Dresden", ak:10, partien:(12*4*9), kampflos:61})

MERGE (hoyerswerda:Verein { name:"FVS ASP Hoyerswerda", bezirk:"Dresden" })
MERGE (heidenau:Verein { name:"Schachklub Heidenau", bezirk:"Dresden" })
MERGE (gwdresden:Verein { name:"SG Grün-Weiß Dresden", bezirk:"Dresden" })
MERGE (bautzen:Verein { name:"SC Einheit Bautzen", bezirk:"Dresden" })
MERGE (ddleuben:Verein { name:"SV Dresden-Leuben", bezirk:"Dresden" })
MERGE (priestewitz:Verein { name:"SV Traktor Priestewitz", bezirk:"Dresden" })
MERGE (ddstriesen:Verein { name:"SV Dresden-Striesen", bezirk:"Dresden" })
MERGE (tudresden:Verein { name:"USV TU Dresden", bezirk:"Dresden" })
MERGE (altenberg:Verein { name:"SSV Altenberg", bezirk:"Dresden" })
MERGE (freital:Verein { name:"SV Freital", bezirk:"Dresden" })
MERGE (radebeul:Verein { name:"BSV Chemie Radebeul", bezirk:"Dresden" })
MERGE (oberland:Verein { name:"SC 1994 Oberland", bezirk:"Dresden" })
MERGE (bannewitz:Verein { name:"SV Bannewitz", bezirk:"Dresden" })
MERGE (smf:Verein { name:"Schach macht fit", bezirk:"Dresden" })
MERGE (großdrebnitz:Verein { name:"SG Großdrebnitz", bezirk:"Dresden" })
MERGE (coswig:Verein { name:"TuS Coswig 1920", bezirk:"Dresden" })
MERGE (gersdorf:Verein { name:"TuS 1890 Gersdorf-Möhrsdorf", bezirk:"Dresden" })
MERGE (goerlitz:Verein { name:"SV Görlitz 1990", bezirk:"Dresden" })
MERGE (seeblick:Verein { name:"Schachzentrum Seeblick e. V.", bezirk:"Dresden" })
MERGE (pirna:Verein { name:"Fortschritt Pirna", bezirk:"Dresden" })

MERGE (plauen:Verein { name:"Schachklub König Plauen", bezirk:"Chemnitz" })
MERGE (usgchemnitz:Verein { name:"USG Chemnitz", bezirk:"Chemnitz" })
MERGE (scaufbau:Verein { name:"Chemnitzer SC Aufbau`95", bezirk:"Chemnitz" })
MERGE (markneukirchen:Verein { name:"SV Markneukirchen", bezirk:"Chemnitz" })
MERGE (muldentalwilkau:Verein { name:"Muldental Wilkau-Haßlau", bezirk:"Chemnitz" })
MERGE (niederwiesa:Verein { name:"SV Grün-W. Niederwiesa", bezirk:"Chemnitz" })

MERGE (lindenau:Verein { name:"SC Leipzig-Lindenau", bezirk:"Leipzig" })
MERGE (vfbleipzig:Verein { name:"VfB Schach Leipzig e.V.", bezirk:"Leipzig" })
MERGE (sgl:Verein { name:"Schachgemeinschaft Leipzig", bezirk:"Leipzig" })
MERGE (kitzscher:Verein { name:"TSV Kitzscher", bezirk:"Leipzig" })
MERGE (bsgleipzig:Verein { name:"BSG Grün-Weiß Leipzig e.V.", bezirk:"Leipzig" })
MERGE (grimma:Verein { name:"SV 1919 Grimma", bezirk:"Leipzig" })
MERGE (turmleipzig:Verein { name:"SG Turm Leipzig", bezirk:"Leipzig" })

MERGE (s2018slu20)-[:IN ]->(saison2018)
// Finale 1-4: https://svs.portal64.de/ergebnisse/show/2018/1695/tabelle/
MERGE (tudresden)-[:TEILNAHME { team:1, platz:1, kampflos:0 }]->(s2018slu20)
MERGE (sgl)-[:TEILNAHME { team:1, platz:2, kampflos:0 }]->(s2018slu20)
MERGE (plauen)-[:TEILNAHME { team:1, platz:3, kampflos:0 }]->(s2018slu20)
MERGE (ddleuben)-[:TEILNAHME { team:1, platz:4, kampflos:0 }]->(s2018slu20)
MERGE (hoyerswerda)-[:TEILNAHME { team:1, platz:5, kampflos:8 }]->(s2018slu20)
MERGE (gwdresden)-[:TEILNAHME { team:1, platz:6, kampflos:2 }]->(s2018slu20)
MERGE (ddstriesen)-[:TEILNAHME { team:1, platz:7, kampflos:5 }]->(s2018slu20)
MERGE (coswig)-[:TEILNAHME { team:1, platz:8, kampflos:0 }]->(s2018slu20)

MERGE (s2018slu20z)-[:IN ]->(saison2018)
MERGE (grimma)-[:TEILNAHME { team:1, platz:1, kampflos:0 }]->(s2018slu20z)
MERGE (bsgleipzig)-[:TEILNAHME { team:1, platz:2, kampflos:0 }]->(s2018slu20z)
MERGE (sgl)-[:TEILNAHME { team:2, platz:3, kampflos:2 }]->(s2018slu20z)
MERGE (niederwiesa)-[:TEILNAHME { team:1, platz:4, kampflos:0 }]->(s2018slu20z)

MERGE (s2018ddu20)-[:IN ]->(saison2018)
MERGE (oberland)-[:TEILNAHME { team:1, platz:1, kampflos:1 }]->(s2018ddu20)
MERGE (ddstriesen)-[:TEILNAHME { team:2, platz:2, kampflos:1 }]->(s2018ddu20)
MERGE (ddleuben)-[:TEILNAHME { team:2, platz:3, kampflos:0 }]->(s2018ddu20)
MERGE (großdrebnitz)-[:TEILNAHME { team:1, platz:4, kampflos:0 }]->(s2018ddu20)
MERGE (ddstriesen)-[:TEILNAHME { team:3, platz:5, kampflos:8 }]->(s2018ddu20)

MERGE (s2018slu16)-[:IN ]->(saison2018)
MERGE (sgl)-[:TEILNAHME { team:1, platz:1, kampflos:0 }]->(s2018slu16)
MERGE (plauen)-[:TEILNAHME { team:1, platz:2, kampflos:0 }]->(s2018slu16)
MERGE (tudresden)-[:TEILNAHME { team:1, platz:3, kampflos:0 }]->(s2018slu16)
MERGE (usgchemnitz)-[:TEILNAHME { team:1, platz:4, kampflos:0 }]->(s2018slu16)
MERGE (ddleuben)-[:TEILNAHME { team:1, platz:5, kampflos:0 }]->(s2018slu16)
MERGE (bsgleipzig)-[:TEILNAHME { team:1, platz:6, kampflos:1 }]->(s2018slu16)
MERGE (grimma)-[:TEILNAHME { team:1, platz:7, kampflos:0 }]->(s2018slu16)
MERGE (turmleipzig)-[:TEILNAHME { team:1, platz:8, kampflos:1 }]->(s2018slu16)
MERGE (muldentalwilkau)-[:TEILNAHME { team:1, platz:9, kampflos:0 }]->(s2018slu16)
MERGE (sgl)-[:TEILNAHME { team:2, platz:10, kampflos:0 }]->(s2018slu16)

MERGE (s2018ddu16)-[:IN ]->(saison2018)
MERGE (hoyerswerda)-[:TEILNAHME { team:1, platz:1, kampflos:0 }]->(s2018ddu16)
MERGE (ddstriesen)-[:TEILNAHME { team:1, platz:2, kampflos:0 }]->(s2018ddu16)
MERGE (großdrebnitz)-[:TEILNAHME { team:1, platz:3, kampflos:2 }]->(s2018ddu16)
MERGE (oberland)-[:TEILNAHME { team:1, platz:4, kampflos:0 }]->(s2018ddu16)
MERGE (heidenau)-[:TEILNAHME { team:1, platz:5, kampflos:0 }]->(s2018ddu16)

MERGE (s2018ddu16ka)-[:IN ]->(saison2018)
MERGE (tudresden)-[:TEILNAHME { team:2, platz:1, kampflos:0 }]->(s2018ddu16ka)
MERGE (goerlitz)-[:TEILNAHME { team:1, platz:2, kampflos:0 }]->(s2018ddu16ka)
MERGE (smf)-[:TEILNAHME { team:1, platz:3, kampflos:2 }]->(s2018ddu16ka)
MERGE (hoyerswerda)-[:TEILNAHME { team:2, platz:4, kampflos:8 }]->(s2018ddu16ka)

MERGE (s2018ddu16kb)-[:IN ]->(saison2018)
MERGE (gwdresden)-[:TEILNAHME { team:1, platz:1, kampflos:2 }]->(s2018ddu16kb)
MERGE (ddleuben)-[:TEILNAHME { team:2, platz:2, kampflos:0 }]->(s2018ddu16kb)
MERGE (priestewitz)-[:TEILNAHME { team:1, platz:3, kampflos:0 }]->(s2018ddu16kb)
MERGE (coswig)-[:TEILNAHME { team:1, platz:4, kampflos:0 }]->(s2018ddu16kb)
MERGE (gwdresden)-[:TEILNAHME { team:2, platz:5, kampflos:2 }]->(s2018ddu16kb)
MERGE (ddstriesen)-[:TEILNAHME { team:2, platz:6, kampflos:6 }]->(s2018ddu16kb)

MERGE (s2018ddu14)-[:IN ]->(saison2018)
MERGE (hoyerswerda)-[:TEILNAHME { team:1, platz:1, kampflos:0 }]->(s2018ddu14)
MERGE (tudresden)-[:TEILNAHME { team:2, platz:2, kampflos:0 }]->(s2018ddu14)
MERGE (tudresden)-[:TEILNAHME { team:1, platz:3, kampflos:8 }]->(s2018ddu14)
MERGE (ddstriesen)-[:TEILNAHME { team:1, platz:4, kampflos:9 }]->(s2018ddu14)

MERGE (s2018ddu14k)-[:IN ]->(saison2018)
MERGE (coswig)-[:TEILNAHME { team:1, platz:1, kampflos:0 }]->(s2018ddu14k)
MERGE (ddleuben)-[:TEILNAHME { team:1, platz:2, kampflos:0 }]->(s2018ddu14k)
MERGE (bannewitz)-[:TEILNAHME { team:1, platz:3, kampflos:0 }]->(s2018ddu14k)
MERGE (heidenau)-[:TEILNAHME { team:1, platz:4, kampflos:2 }]->(s2018ddu14k)
MERGE (smf)-[:TEILNAHME { team:1, platz:5, kampflos:4 }]->(s2018ddu14k)
MERGE (gwdresden)-[:TEILNAHME { team:1, platz:6, kampflos:6 }]->(s2018ddu14k)
MERGE (großdrebnitz)-[:TEILNAHME { team:1, platz:7, kampflos:0 }]->(s2018ddu14k)

MERGE (s2018ddu12)-[:IN ]->(saison2018)
MERGE (tudresden)-[:TEILNAHME { team:1, platz:1, kampflos:0 }]->(s2018ddu12)
MERGE (seeblick)-[:TEILNAHME { team:1, platz:2, kampflos:0 }]->(s2018ddu12)
MERGE (coswig)-[:TEILNAHME { team:1, platz:3, kampflos:0 }]->(s2018ddu12)
MERGE (ddleuben)-[:TEILNAHME { team:1, platz:4, kampflos:0 }]->(s2018ddu12)
MERGE (heidenau)-[:TEILNAHME { team:1, platz:5, kampflos:0 }]->(s2018ddu12)
MERGE (priestewitz)-[:TEILNAHME { team:1, platz:6, kampflos:0 }]->(s2018ddu12)
MERGE (hoyerswerda)-[:TEILNAHME { team:1, platz:7, kampflos:0 }]->(s2018ddu12)
MERGE (gwdresden)-[:TEILNAHME { team:1, platz:8, kampflos:0 }]->(s2018ddu12)

MERGE (s2018ddu12ka)-[:IN ]->(saison2018)
MERGE (gwdresden)-[:TEILNAHME { team:2, platz:1, kampflos:0 }]->(s2018ddu12ka)
MERGE (coswig)-[:TEILNAHME { team:2, platz:2, kampflos:0 }]->(s2018ddu12ka)
MERGE (tudresden)-[:TEILNAHME { team:2, platz:3, kampflos:0 }]->(s2018ddu12ka)
MERGE (priestewitz)-[:TEILNAHME { team:2, platz:4, kampflos:2 }]->(s2018ddu12ka)
MERGE (altenberg)-[:TEILNAHME { team:1, platz:5, kampflos:0 }]->(s2018ddu12ka)
MERGE (smf)-[:TEILNAHME { team:1, platz:6, kampflos:0 }]->(s2018ddu12ka)
MERGE (freital)-[:TEILNAHME { team:1, platz:7, kampflos:0 }]->(s2018ddu12ka)

MERGE (s2018ddu12kb)-[:IN ]->(saison2018)
MERGE (pirna)-[:TEILNAHME { team:1, platz:1, kampflos:0 }]->(s2018ddu12kb)
MERGE (ddstriesen)-[:TEILNAHME { team:1, platz:2, kampflos:0 }]->(s2018ddu12kb)
MERGE (bautzen)-[:TEILNAHME { team:1, platz:3, kampflos:0 }]->(s2018ddu12kb)
MERGE (oberland)-[:TEILNAHME { team:1, platz:4, kampflos:0 }]->(s2018ddu12kb)
MERGE (ddleuben)-[:TEILNAHME { team:2, platz:5, kampflos:0 }]->(s2018ddu12kb)
MERGE (ddstriesen)-[:TEILNAHME { team:2, platz:6, kampflos:0 }]->(s2018ddu12kb)
MERGE (coswig)-[:TEILNAHME { team:3, platz:7, kampflos:0 }]->(s2018ddu12kb)

MERGE (s2018ddu10)-[:IN ]->(saison2018)
MERGE (tudresden)-[:TEILNAHME { team:1, platz:1, kampflos:0 }]->(s2018ddu10)
MERGE (coswig)-[:TEILNAHME { team:1, platz:2, kampflos:1 }]->(s2018ddu10) // 1
MERGE (ddleuben)-[:TEILNAHME { team:1, platz:3, kampflos:0 }]->(s2018ddu10)
MERGE (priestewitz)-[:TEILNAHME { team:1, platz:4, kampflos:0 }]->(s2018ddu10)
MERGE (coswig)-[:TEILNAHME { team:3, platz:5, kampflos:0 }]->(s2018ddu10)
MERGE (ddstriesen)-[:TEILNAHME { team:1, platz:6, kampflos:0 }]->(s2018ddu10)
MERGE (gwdresden)-[:TEILNAHME { team:1, platz:7, kampflos:0 }]->(s2018ddu10)
MERGE (seeblick)-[:TEILNAHME { team:1, platz:8, kampflos:0 }]->(s2018ddu10)
MERGE (oberland)-[:TEILNAHME { team:1, platz:9, kampflos:3+0 }]->(s2018ddu10)
MERGE (smf)-[:TEILNAHME { team:1, platz:10, kampflos:0 }]->(s2018ddu10)
MERGE (ddstriesen)-[:TEILNAHME { team:2, platz:11, kampflos:0 }]->(s2018ddu10)
MERGE (tudresden)-[:TEILNAHME { team:2, platz:12, kampflos:3+0+0 }]->(s2018ddu10)
MERGE (freital)-[:TEILNAHME { team:1, platz:13, kampflos:0 }]->(s2018ddu10)
MERGE (smf)-[:TEILNAHME { team:2, platz:14, kampflos:3+0+3 }]->(s2018ddu10) // 3
MERGE (hoyerswerda)-[:TEILNAHME { team:1, platz:15, kampflos:0 }]->(s2018ddu10)
MERGE (bautzen)-[:TEILNAHME { team:1, platz:16, kampflos:3+0 }]->(s2018ddu10)
MERGE (heidenau)-[:TEILNAHME { team:3, platz:17, kampflos:2+0 }]->(s2018ddu10)
MERGE (ddleuben)-[:TEILNAHME { team:2, platz:18, kampflos:0 }]->(s2018ddu10)
MERGE (priestewitz)-[:TEILNAHME { team:2, platz:19, kampflos:1+6+6 }]->(s2018ddu10) // 6
MERGE (coswig)-[:TEILNAHME { team:2, platz:20, kampflos:3+0+0 }]->(s2018ddu10)
MERGE (heidenau)-[:TEILNAHME { team:1, platz:21, kampflos:3+6 }]->(s2018ddu10) // 6
MERGE (heidenau)-[:TEILNAHME { team:2, platz:22, kampflos:3 }]->(s2018ddu10) // 3
MERGE (großdrebnitz)-[:TEILNAHME { team:1, platz:23, kampflos:12+0 }]->(s2018ddu10)
MERGE (gwdresden)-[:TEILNAHME { team:2, platz:24, kampflos:3 }]->(s2018ddu10) // 3

// ╒═════════════════════════════════════════════╤════════════════════════╕
// │Bezirksliga Dresden U10 2018/19              │Verein                  │
// ╞═════════════════════════════════════════════╪════════════════════════╡
// │[:TEILNAHME {kampflos: 13,platz: 19,team: 2}]│"SV Traktor Priestewitz"│
// ├─────────────────────────────────────────────┼────────────────────────┤
// │[:TEILNAHME {kampflos: 12,platz: 23,team: 1}]│"SG Großdrebnitz"       │
// ├─────────────────────────────────────────────┼────────────────────────┤
// │[:TEILNAHME {kampflos: 9,platz: 21,team: 1}] │"Schachklub Heidenau"   │
// ├─────────────────────────────────────────────┼────────────────────────┤
// │[:TEILNAHME {kampflos: 6,platz: 14,team: 2}] │"Schach macht fit"      │
// ├─────────────────────────────────────────────┼────────────────────────┤
// │[:TEILNAHME {kampflos: 3,platz: 22,team: 2}] │"Schachklub Heidenau"   │
// ├─────────────────────────────────────────────┼────────────────────────┤
// │[:TEILNAHME {kampflos: 3,platz: 24,team: 2}] │"SG Grün-Weiß Dresden"  │
// ├─────────────────────────────────────────────┼────────────────────────┤
// │[:TEILNAHME {kampflos: 3,platz: 16,team: 1}] │"SC Einheit Bautzen"    │
// ├─────────────────────────────────────────────┼────────────────────────┤
// │[:TEILNAHME {kampflos: 3,platz: 12,team: 2}] │"USV TU Dresden"        │
// ├─────────────────────────────────────────────┼────────────────────────┤
// │[:TEILNAHME {kampflos: 3,platz: 9,team: 1}]  │"SC 1994 Oberland"      │
// ├─────────────────────────────────────────────┼────────────────────────┤
// │[:TEILNAHME {kampflos: 3,platz: 20,team: 2}] │"TuS Coswig 1920"       │
// ├─────────────────────────────────────────────┼────────────────────────┤
// │[:TEILNAHME {kampflos: 2,platz: 17,team: 3}] │"Schachklub Heidenau"   │
// ├─────────────────────────────────────────────┼────────────────────────┤
// │[:TEILNAHME {kampflos: 1,platz: 2,team: 1}]  │"TuS Coswig 1920"       │
// └─────────────────────────────────────────────┴────────────────────────┘