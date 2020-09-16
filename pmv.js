function calcPMV() {
  const AL = 1.0; //活動量[met]
  const CLO = 1.0; //着衣量[clo]
  const TA = 25; //温度[℃]
  const TR = 25; //平均放射温度＜MRT＞[℃]
  const VA = 0.5; //気流速度[m/s]
  const RH = 50; //相対湿度[％]

  //PMV 計算準備
  let m = AL * 58.15;
  let lcl = CLO;
  let w = 0; //外部仕事 W＝0 [W/㎡]とする。
  //let pa = (RH / 100 * Math.exp(18.6686 - 4030.18 / (TA + 235))) / 0.00750062
  let ppk = 673.4 - 1.8 * TA;
  let ppa = 3.2437814 + 0.00326014 * ppk + 2.00658 * 0.000000001 * ppk * ppk * ppk;
  let ppb = (1165.09 - ppk) * (1 + 0.00121547 * ppk);
  let pa = RH / 100 * 22105.8416 / Math.exp(2.302585 * ppk * ppa / ppb) * 1000.0;
  let eps = 0.00001;
  let mv = m - w;

  //FCL＝着衣表面積／裸体表面積の比
  let fcl = 1.0 + 0.2 * lcl;
  if (lcl > 0.5) {
    fcl = 1.05 + 0.1 * lcl;
  };
  //衣服表面温度TCLの初期値設定
  let tcl = TA;
  let tcla = tcl;
  let noi = 1;

  //着衣表面温度の計算
  let hc = 0;
  do {
    tcla = 0.8 * tcla + 0.2 * tcl;
    hc = 12.1 * Math.sqrt(VA);
    if (2.38 * Math.sqrt(Math.sqrt(Math.abs(tcl - TA))) > hc) {
      hc = 2.38 * Math.sqrt(Math.sqrt(Math.abs(tcl - TA)));
    };
    tcl = 35.7 - 0.028 * mv - 0.155 * lcl * (3.96 * 0.00000001 * fcl * (Math.pow(tcla + 273, 4) - Math.pow(TR + 273, 4)) + fcl * hc * (tcla - TA));
    noi = noi + 1;
    if (noi > 150) {
      return {
        "pmv": 999990.999,
        "ppd": 100.0
      };
    }
  } while (Math.abs(tcla - tcl) > eps);

  //PMVの計算
  let pm1 = 3.96 * 0.00000001 * fcl * (Math.pow(tcl + 273, 4) - Math.pow(TR + 273, 4));
  let pm2 = fcl * hc * (tcl - TA);
  let pm3 = 0.303 * Math.exp(-0.036 * m) + 0.028;
  let pm4 = 0;
  if (mv > 58.15) {
    pm4 = 0.42 * (mv - 58.15);
  };
  let pmv = pm3 * (mv - 3.05 * 0.001 * (5733 - 6.99 * mv - pa) - pm4 - 1.7 * 0.00001 * m * (5867 - pa) - 0.0014 * m * (34 - TA) - pm1 - pm2);
  //PRINT PMV
  if (Math.abs(pmv) > 3) {
    return {
      "pmv": pmv,
      "ppd": 100.0
    };
  } else {
    let ppd = 100 - 95 * Math.exp(-0.0335 * Math.pow(pmv, 4) - 0.2179 * Math.pow(pmv, 2));
    return {
      "pmv": pmv,
      "ppd": ppd
    };
  }
}


console.log(calcPMV());
