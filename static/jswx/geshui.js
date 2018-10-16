/**
 * 初始化方法
 * 
 * @author yanyi
 * 
 * 个税计算器
 */

var default_shebao_base = 2366; //社保缴费基数
var default_max_base = 12615; //社保公积金封顶数

var ylbxbl = 8; //养老保险比例
var ylbl = 2; //医疗保险比例
var sybxbl = 1; //失业保险比例
var gjjbl = 5; //公积金比例

$(document).ready(function() {
	
	/*if (!is_weixn()){
		alert('页面只能在微信浏览器中打开！');
	}*/
	
	var params = getParamsFromHref();
	var sbgjj = params["sbgjj"]; //社保公积金
	var sqysr = params["sqysr"]; //税前月收入
	var updBl =params["updBl"];
	$("#sgq").attr("style","border-bottom: 2px solid #35bef4");
	$("#sgh").attr("style","border-bottom: 1px solid #D3D3D3");
	if(updBl=="updBlsgq"){
		$("#sgq").attr("style","border-bottom: 2px solid #35bef4");
		$("#sgh").attr("style","border-bottom: 1px solid #D3D3D3");
		$("#sgqView").show();
		$("#sghdiv").css("display","none");
		$("#sghView").hide();
	}else if(updBl=="updBlsgh"){
		$("#sgh").attr("style","border-bottom: 2px solid #35bef4");
		$("#sgq").attr("style","border-bottom: 1px solid #D3D3D3");
		$("#sgqView").hide();
		$("#sghdiv").css("display","block");
		$("#sghView").show();
	}
	
	if (sbgjj != undefined){
		if(updBl=="updBlsgq"){
			$("#sbgjj").val(parseFloat(sbgjj).toFixed(2)); //社保公积金
			$("#sqygzxj").val(sqysr); //税改前月收入
		}else if(updBl=="updBlsgh"){
			$("#sbgjjSgh").val(parseFloat(sbgjj).toFixed(2)); //社保公积金
			$("#sqygzxjSgh").val(sqysr); //税改后月收入
		}
		
		
		//各项比例
		ylbxbl = parseFloat(params["ylbxbl"]);
		ylbl = parseFloat(params["ylbl"]);
		sybxbl = parseFloat(params["sybxbl"]);
		gjjbl = parseFloat(params["gjjbl"]);
		
	}
});

/**
 * 验证空
 * @returns {Boolean}
 */
function isValidate(obj) {
	var sgqVld = obj.id;
	if(sgqVld=="sgqjs"){ //税改前计算
		var sqygzxj = $("#sqygzxj").val();// 税前月收入
		var fykce = $("#fykce").val();// 个税起征点
		var sbgjj = $("#sbgjj").val();// 社保公积金
		
		if (sqygzxj.trim() == "") {
			$("#message").text("请输入税前月工资薪金！");
			return false;
		} else if (isNaN(sqygzxj)) {
			$("#message").text("输入的不是合法的税前月工资薪金！");
			return false;
		}else if (fykce.trim() == "") {
			$("#message").text("请输入个税起征点（费用扣除额）！");
			return false;
		} else if (sbgjj.trim() == ""){
			$("#sbgjj").val(calculateSbgjj(sqygzxj));
		}
	}else if(sgqVld=="sghjs"){
		var sqygzxjSgh = $("#sqygzxjSgh").val();// 税前月收入
		var fykceSgh = $("#fykceSgh").val();// 个税起征点
		var sbgjjSgh = $("#sbgjjSgh").val();// 社保公积金
		
		if (sqygzxjSgh.trim() == "") {
			$("#messageSgh").text("请输入税前月工资薪金！");
			return false;
		} else if (isNaN(sqygzxjSgh)) {
			$("#messageSgh").text("输入的不是合法的税前月工资薪金！");
			return false;
		}else if (fykceSgh.trim() == "") {
			$("#messageSgh").text("请输入个税起征点（费用扣除额）！");
			return false;
		} else if (sbgjjSgh.trim() == ""){
			$("#sbgjjSgh").val(calculateSbgjj(sqygzxjSgh));
		}
	}
	$("#message").text(" ");
	
	calculateGeShui(sgqVld);
}

/**
 * 计算社保公积金
 * 
 * @param sqysr 税前月工资
 * @return 社保公积金
 */
function calculateSbgjj(sqysr) {
	var sbgjj = 0; //社保公积金缴纳总额

	var sb = 0; //社保缴纳额度
	var gjj = 0; //公积金缴纳额度

	// 1、获取社保比例之和
	var sb_percent = parseFloat((ylbxbl + ylbl + sybxbl) / 100);
	// 2、获取公积金比例
	var gjj_percent = parseFloat(gjjbl /100);
	// 3、税前月收入 <= 2336(社保基数)
	if (sqysr < default_shebao_base) {
		// 工资小于社保缴费基数时，社保按照缴费基数计算:缴费基数 * 社保比例和
		sb = default_shebao_base * sb_percent;
		gjj = sqysr * gjj_percent;
	} else if (sqysr >= default_shebao_base && sqysr <= default_max_base) {
		// 税前月收入 <= 12615（公积金社保封顶数）
		sb = sqysr * sb_percent;
		gjj = sqysr * gjj_percent;
	} else {// 税前月收入 > 12615（公积金社保封顶数）
		sb = default_max_base * sb_percent;
		gjj = default_max_base * gjj_percent;
	}
	
	sbgjj = sb + gjj;

	return parseFloat(sbgjj).toFixed(2);
}

/**
 * 个税计算 ：需要交个税的金额 = 税前月收入 - 社保公积金 - 个税起征点 个税金额 = 需要交个税的金额 * 税率 - 速算扣除数
 * 
 * @param sqysr 税前月收入
 * @param gsqzd 个税起征点
 * @param sbgjj 社保公积金
 * 税改前
 */
function calculateGeShui(sgqVld) {
	var sqysr="";
	var gsqzd="";
	var sbgjj="";
	
	var over = 0; // 超出个税起征点部分
	var yjgs = 0;// 应缴个税
	var rate = 0;// 税率
	var kcs = 0;// 速算扣除数
	
	if(sgqVld=="sgqjs"){ //税改前计算
		
		 sqysr = $("#sqygzxj").val();// 税前月收入
		 gsqzd = $("#fykce").val();// 个税起征点
		 sbgjj = $("#sbgjj").val();// 社保公积金
		 over =sqysr - sbgjj - gsqzd;
		 if (over <= 0) {
				yjgs = 0;
			} else if (over <= 1500) {
				rate = 0.03;
				kcs = 0;
			} else if (over <= 4500) {
				rate = 0.1;
				kcs = 105;
			} else if (over <= 9000) {
				rate = 0.2;
				kcs = 555;
			} else if (over <= 35000) {
				rate = 0.25;
				kcs = 1005;
			} else if (over <= 55000) {
				rate = 0.3;
				kcs = 2755;
			} else if (over <= 80000) {
				rate = 0.35;
				kcs = 5505;
			} else {
				rate = 0.45;
				kcs = 13505;
			}
		 
	}else if(sgqVld=="sghjs"){ //税改后
		 sqysr = $("#sqygzxjSgh").val();// 税前月收入
		 gsqzd = $("#fykceSgh").val();// 个税起征点
		 sbgjj = $("#sbgjjSgh").val();// 社保公积金
		 over =sqysr - sbgjj - gsqzd;
		 if (over <= 0) {
				yjgs = 0;
			} else if (over <= 3000) {
				rate = 0.03;
				kcs = 0;
			} else if (over <= 12000) {
				rate = 0.1;
				kcs = 210;
			} else if (over <= 25000) {
				rate = 0.2;
				kcs = 1410;
			} else if (over <= 35000) {
				rate = 0.25;
				kcs = 2660;
			} else if (over <= 55000) {
				rate = 0.3;
				kcs = 4410;
			} else if (over <= 80000) {
				rate = 0.35;
				kcs = 7160;
			} else {
				rate = 0.45;
				kcs = 15160;
			}
	}
	
	// 应缴个税
	yjgs = over * rate - kcs;
	
	var message = "";
	
	// 税后月收入
	var shysr = sqysr - sbgjj - yjgs;
	if (shysr > 0) {
		message += "税后月收入" + parseFloat(shysr).toFixed(2) + "元，";
	} else {
		message += "税后月收入0元，";// 税后月收入
	}
	
	//应征个税
	if (yjgs > 0) {
		message += "应缴纳个人所得税" + parseFloat(yjgs).toFixed(2) + "元。";
	} else {
		message += "应缴纳个人所得税0元。";
	}
	
	if(sgqVld=="sgqjs"){ //税改前计算
		$("#message").text(message);
	}else if(sgqVld=="sghjs"){ //税改后
		$("#messageSgh").text(message);
	}
}

/**
 * 是否外籍选中事件
 */
function sfwjOnchange(selChk){
	if (selChk.value == "10"){
		$("#fykce").val("3500");
		$("#sbgjj").val("");
		$("#sbgjj").removeAttr("disabled");
		$("#updBl").show();
	} else {
		$("#fykce").val("4800");
		$("#sbgjj").val("0");
		$("#sbgjj").attr({"disabled":"disabled"});
		$("#updBl").hide();
	}
	$("#message").text('');
}

/**
 * 点击修改比例按钮事件
 */
function updBl(obj){
	var updBl=obj.id;
	var sqysr="";
	if(updBl=="updBlsgq"){
		 sqysr = $("#sqygzxj").val();// 税前月收入
		
		if (sqysr.trim() == ""){
			$("#message").text("请输入税前月工资薪金！");
			return false;
		}
		$("#message").text(" ");
	}else if(updBl=="updBlsgh"){
		 sqysr = $("#sqygzxjSgh").val();// 税前月收入
		
		if (sqysr.trim() == ""){
			$("#messageSgh").text("请输入税前月工资薪金！");
			return false;
		}
		$("#messageSgh").text(" ");
	}
	
	
	var params = "ylbxbl=" + ylbxbl + "&ylbl=" + ylbl + "&sybxbl=" + sybxbl + "&gjjbl=" + gjjbl +"&updBl="+updBl;
	window.location = "indexDetail.jsp?sqysr=" + sqysr + "&" + params;
	
}

/**
 * 税前月工资改变事件
 */
function sqygzChange(txt){
	$("#sbgjj").val('');
	$("#message").text('');
	$("#messageSgh").text('');
	
}
function sqygzChange2(txt){
	$("#message").text('');
	$("#messageSgh").text('');
}

/**
 * 判断是否在微信内置浏览器中打开网页
 * @returns {Boolean} true是在微信中打开 false不是在微信浏览器中打开
 */
function is_weixn(){
	var browserName = navigator.userAgent.toLowerCase();
	if(browserName.match(/MicroMessenger/i) == "micromessenger" || browserName.match(/Windows Phone/i) == "windows phone") { 
		return true; 
	} else { 
		return false; 
	}
}

function sgq(){
	$("#sgq").attr("style","border-bottom: 2px solid #35bef4");
	$("#sgh").attr("style","border-bottom: 1px solid #D3D3D3");
	$("#sgqView").show();
	//清空税改后
	$("#sqygzxjSgh").val("");
	$("#sbgjjSgh").val("");
	$("#messageSgh").text(" ");
	
	$("#sghdiv").css("display","none");
	$("#sghView").hide();
}


function sgh(){
	$("#sgq").attr("style","border-bottom: 1px solid #D3D3D3");
	$("#sgh").attr("style","border-bottom: 2px solid #35bef4");
	//清空税改后
	$("#sqygzxj").val("");
	$("#sbgjj").val("");
	$("#message").text(" ");
	$("#sgqView").hide();
	$("#sghdiv").css("display","block");
	$("#sghView").show();
	
}