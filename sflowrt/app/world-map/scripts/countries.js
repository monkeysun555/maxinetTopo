var scale    = getSystemProperty('world-map.scale')    || 2;
var aggMode  = getSystemProperty('world-map.aggMode')  || 'sum';
var maxFlows = getSystemProperty('world-map.maxFlows') || 1000;
var minValue = getSystemProperty('world-map.minValue') || 0.01;
var agents   = getSystemProperty('world-map.agents')   || 'ALL';
var t        = getSystemProperty('world-map.t')        || 5;
var cc2to3 = {"af":"AFG","ax":"ALA","al":"ALB","dz":"DZA","as":"ASM","ad":"AND","ao":"AGO","ai":"AIA","aq":"ATA","ag":"ATG","ar":"ARG","am":"ARM","aw":"ABW","au":"AUS","at":"AUT","az":"AZE","bs":"BHS","bh":"BHR","bd":"BGD","bb":"BRB","by":"BLR","be":"BEL","bz":"BLZ","bj":"BEN","bm":"BMU","bt":"BTN","bo":"BOL","bq":"BES","ba":"BIH","bw":"BWA","bv":"BVT","br":"BRA","io":"IOT","bn":"BRN","bg":"BGR","bf":"BFA","bi":"BDI","kh":"KHM","cm":"CMR","ca":"CAN","cv":"CPV","ky":"CYM","cf":"CAF","td":"TCD","cl":"CHL","cn":"CHN","cx":"CXR","cc":"CCK","co":"COL","km":"COM","cg":"COG","cd":"COD","ck":"COK","cr":"CRI","ci":"CIV","hr":"HRV","cu":"CUB","cw":"CUW","cy":"CYP","cz":"CZE","dk":"DNK","dj":"DJI","dm":"DMA","do":"DOM","ec":"ECU","eg":"EGY","sv":"SLV","gq":"GNQ","er":"ERI","ee":"EST","et":"ETH","fk":"FLK","fo":"FRO","fj":"FJI","fi":"FIN","fr":"FRA","gf":"GUF","pf":"PYF","tf":"ATF","ga":"GAB","gm":"GMB","ge":"GEO","de":"DEU","gh":"GHA","gi":"GIB","gr":"GRC","gl":"GRL","gd":"GRD","gp":"GLP","gu":"GUM","gt":"GTM","gg":"GGY","gn":"GIN","gw":"GNB","gy":"GUY","ht":"HTI","hm":"HMD","va":"VAT","hn":"HND","hk":"HKG","hu":"HUN","is":"ISL","in":"IND","id":"IDN","ir":"IRN","iq":"IRQ","ie":"IRL","im":"IMN","il":"ISR","it":"ITA","jm":"JAM","jp":"JPN","je":"JEY","jo":"JOR","kz":"KAZ","ke":"KEN","ki":"KIR","kp":"PRK","kr":"KOR","kw":"KWT","kg":"KGZ","la":"LAO","lv":"LVA","lb":"LBN","ls":"LSO","lr":"LBR","ly":"LBY","li":"LIE","lt":"LTU","lu":"LUX","mo":"MAC","mk":"MKD","mg":"MDG","mw":"MWI","my":"MYS","mv":"MDV","ml":"MLI","mt":"MLT","mh":"MHL","mq":"MTQ","mr":"MRT","mu":"MUS","yt":"MYT","mx":"MEX","fm":"FSM","md":"MDA","mc":"MCO","mn":"MNG","me":"MNE","ms":"MSR","ma":"MAR","mz":"MOZ","mm":"MMR","na":"NAM","nr":"NRU","np":"NPL","nl":"NLD","nc":"NCL","nz":"NZL","ni":"NIC","ne":"NER","ng":"NGA","nu":"NIU","nf":"NFK","mp":"MNP","no":"NOR","om":"OMN","pk":"PAK","pw":"PLW","ps":"PSE","pa":"PAN","pg":"PNG","py":"PRY","pe":"PER","ph":"PHL","pn":"PCN","pl":"POL","pt":"PRT","pr":"PRI","qa":"QAT","re":"REU","ro":"ROU","ru":"RUS","rw":"RWA","bl":"BLM","sh":"SHN","kn":"KNA","lc":"LCA","mf":"MAF","pm":"SPM","vc":"VCT","ws":"WSM","sm":"SMR","st":"STP","sa":"SAU","sn":"SEN","rs":"SRB","sc":"SYC","sl":"SLE","sg":"SGP","sx":"SXM","sk":"SVK","si":"SVN","sb":"SLB","so":"SOM","za":"ZAF","gs":"SGS","ss":"SSD","es":"ESP","lk":"LKA","sd":"SDN","sr":"SUR","sj":"SJM","sz":"SWZ","se":"SWE","ch":"CHE","sy":"SYR","tw":"TWN","tj":"TJK","tz":"TZA","th":"THA","tl":"TLS","tg":"TGO","tk":"TKL","to":"TON","tt":"TTO","tn":"TUN","tr":"TUR","tm":"TKM","tc":"TCA","tv":"TUV","ug":"UGA","ua":"UKR","ae":"ARE","gb":"GBR","us":"USA","um":"UMI","uy":"URY","uz":"UZB","vu":"VUT","ve":"VEN","vn":"VNM","vg":"VGB","vi":"VIR","wf":"WLF","eh":"ESH","ye":"YEM","zm":"ZMB","zw":"ZWE"};

setFlow('world-map',{
  keys:'ipsource,ipdestination',
  value:'bytes',
  n:20,
  t:t});

setHttpHandler(function(req) {
   result = [];
   var flows = activeFlows('TOPOLOGY','world-map', maxFlows,minValue,aggMode);
   if(flows) {
     let totals = {};
     for(let i = 0; i < flows.length; i++) {
       var[src,dst] = flows[i].key.split(',');
       let val = flows[i].value;
       totals[src] = (totals[src] || 0) + val;
       totals[dst] = (totals[dst] || 0) + val; 
     }
     for(let cc in totals) {
       result.push({
         'country': geoIPmapping(cc),
         'radius': Math.max(1,Math.log10(totals[cc])*scale)
       }); 
     }
   }


    // let flow = {}
     // flow['ori'] = src;
     // flow['dst'] = dst;
     // flow['volume'] = val;
     // flows[i] = flow;
     // for(let lk in flows){
     //   arcs.push({
     //    'origin': geoIPmapping(flows[lk].ori),
     //    'dst': geoIPmapping(flows[lk].dst),
     //    'widthvalue': Math.max(1,Math.log10(flows[lk].volume)*scale)
     //   }) 
     // }
   return result;
});

function geoIPmapping(ip){
  var country = '';
  if(ip == '10.0.0.1' || ip == '10.0.0.2' || ip == '10.0.0.3'){
    country = 'us';
  }
  else if(ip == '10.0.0.4' || ip == '10.0.0.5' || ip == '10.0.0.6'){
    country = 'cn';
  }

  return country
}

// setHttpHandler(function(req) {
//    result = [];
//    var flows = activeFlows(agents,'world-map',maxFlows,minValue,aggMode);
//    if(flows) {
//      let totals = {};
//      for(let i = 0; i < flows.length; i++) {
//        var[src,dst] = flows[i].key.split(',');
//        let val = flows[i].value;
//        totals[src] = (totals[src] || 0) + val;
//        totals[dst] = (totals[dst] || 0) + val; 
//      }
//      for(let cc in totals) {
//        result.push({
//          'country':cc.toLowerCase(),
//          'radius':Math.max(1,Math.log10(totals[cc])*scale)
//        }); 
//      }
//    }
//    return result;
// });