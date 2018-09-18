var startPosition, endPosition, deltaX, deltaY, moveLength;
var overHeight = false;
var url = "http://www.bjjtat.com/CSRBroker/"
var serverProtocol = {
    protocolId: 5,
    robotHashCode: '2166b7ed7d2e5f7a93b8be20cc44d1c1',
    platformId: 0,
    platformConnType: 6,
    userId: "webchat_" + (new Date()).valueOf(),
    receiverId: '3.3.0',
    talkerId: 0,
    appKey: "2f6d54ff",
    queryType: 0,
    query: '',
    type: 'text',
    modal: 0,
    sendTime: null,
    remoteAddr: null,
    human_agent: 0
};
var voice = {
    localId: '',
    serverId: ''
};
$(function () {
//	window.ontouchstart = function(e) { e.preventDefault(); };
    /**
     * 切换语音和文字发送
     */
    $(".opt1").find(".change").on("click", function () {
        $(".opt1").addClass("dis-none-imp");
        $(".opt2").removeClass("dis-none-imp");
    })
    $(".opt2").find(".change").on("click", function () {
        $(".opt2").addClass("dis-none-imp");
        $(".opt1").removeClass("dis-none-imp");
    })
    /**
     * 调用语音录入接口
     */
        //手指按下
    var currentDate, minsstart, minsend;
    $(".voice").on("touchstart", function (e) {
        currentDate = new Date();
        minsstart = currentDate.getMinutes() * 60 + currentDate.getSeconds();
//		console.log(minsstart);
        $(".pop-send").removeClass("dis-none-imp");
        var touch = e.originalEvent.touches[0];
        startPosition = {
            x: touch.pageX,
            y: touch.pageY
        }
        wx.startRecord({
            cancel: function () {
                $(".pop-send").addClass("dis-none-imp");
                meng.alert('用户拒绝授权录音');
            }
        });
        e.preventDefault();
    })
    /*//手指移动
    $(".voice").on("touchmove",function(e){
        var touch = e.originalEvent.touches[0];
        endPosition = {
            x: touch.pageX,
            y: touch.pageY
        }

        deltaX = endPosition.x - startPosition.x;
        deltaY = endPosition.y - startPosition.y;
        moveLength = deltaY<0?Math.sqrt(Math.pow(Math.abs(deltaX), 2) + Math.pow(Math.abs(deltaY), 2)):Math.sqrt(Math.pow(Math.abs(deltaX), 2) + Math.pow(Math.abs(deltaY), 2));
//        console.log(moveLength);
        if(moveLength>50){
            $(".pop-send").addClass("dis-none-imp");
            $(".pop-cancel").removeClass("dis-none-imp");
            //超过滑动距离取消录音
            overHeight = true;
        }
    })*/
    //手指离开
    $(".voice").on("touchend", function (e) {
        e.preventDefault();
        currentDate = new Date();
        minsend = currentDate.getMinutes() * 60 + currentDate.getSeconds();
//		console.log(minsend);
        if (minsend - minsstart < 1) {
            meng.alert("录音时间太短");
            $(".pop-send").addClass("dis-none-imp");
            $(".pop-cancel").addClass("dis-none-imp");
            wx.stopRecord({
                success: function (res) {
                    voice.localId = res.localId;
                },
                fail: function (res) {
                    meng.alert(JSON.stringify(res));
                }
            });
            return;
        }
        $(".pop-send").addClass("dis-none-imp");
        $(".pop-cancel").addClass("dis-none-imp");
        //语音发送
        wx.stopRecord({
            success: function (res) {
                voice.localId = res.localId;
                showAskVoice(res.localId);
                if (overHeight == false) {
                    //语音识别
                    wx.translateVoice({
                        localId: voice.localId, // 需要识别的音频的本地Id，由录音相关接口获得
                        isShowProgressTips: 1, // 默认为1，显示进度提示
                        success: function (res) {
//					        alert(res.translateResult); // 语音识别的结果
                            showAnswerMsg("识别出您的语音：" + res.translateResult);
                            send(res.translateResult);
                        }
                    });
                    /*//先上传到微信服务器
                    wx.uploadVoice({
                        localId: voice.localId, // 需要上传的音频的本地ID，由stopRecord接口获得
                        isShowProgressTips: 1, // 默认为1，显示进度提示
                        success: function (res) {
                            var serverId = res.serverId; // 返回音频的服务器端ID
                            //
                            $("#msg").val(serverId);
                        }
                    });*/
                }
            },
            fail: function (res) {
                meng.alert(JSON.stringify(res));
            }
        });
        e.preventDefault();
    })

    //监听录音自动停止
    wx.onVoiceRecordEnd({
        complete: function (res) {
            voice.localId = res.localId;
            meng.alert('录音已停止');
        }
    });


    /**
     * 文字发送
     */
    $(".send-btn").on("click", function () {
        var num_id=-1
        var msg = $("#msg").val();
        showAsk(num_id,msg);
    })
})

/**
 * 发送成功返回
 * @param result
 */
function serverResponseSuccess(result) {
    // var singleNode =result.singleNode;//单一回答节点
    // var vagueNode=result.vagueNode;//vagueNode多选回答节点
    // var answerTypeId=result.answerTypeId;
    // var answer="";
    // if(vagueNode&&answerTypeId==6&&vagueNode.itemList&&vagueNode.itemList.length>0){
    //    answer=result.singleNode.answerMsg;
    //
    //    var promptVagueMsg=vagueNode.promptVagueMsg;
    //    answer+="<br/>"+promptVagueMsg;
    //    for(var i=0; i<vagueNode.itemList.length; i++){
    // 	   var items=vagueNode.itemList[i];
    // 	   answer+='<br/><a href="#" qnum='+items.num+' onclick=showAsk('+items.num+')>' +"["+items.num+"]"+ items.question +'</a>';
    //   }
    //
    // }else if(vagueNode&&vagueNode.itemList&&vagueNode.itemList.length>0){
    //   	answer=vagueNode.promptVagueMsg;
    //   	for(var i=0; i<vagueNode.itemList.length; i++){
    //   		var items=vagueNode.itemList[i];
    //   		answer=answer + '<br/><a href="#" qnum='+items.num+' onclick=showAsk('+items.num+')>' +"["+items.num+"]"+ items.question +'</a>';
    //   	}
    //   	answer+="<br/>"+(vagueNode.endVagueMsg==null?"":vagueNode.endVagueMsg);
    // } else if(singleNode.isRichText==1&&singleNode.list&&singleNode.list.length>0){
    //   answer="图文不支持展示";
    // }else{
    //   answer=singleNode.answerMsg;
    // }
    showAnswerMsg(result.data);
}

/**
 * 回答
 * @param msg
 */
function showAnswerMsg(msg) {
    var sendHTML = '<div class="group clear left">' +
        '<img src="/static/images/portrait.jpg" class="portrait left" alt=""/>' +
        '<p class="message left">' + msg + '</p>' +
        '</div>';
    $(".content").append(sendHTML);
    //滚动到底部
    $(".content").scrollTop($(".content")[0].scrollHeight);
}

/**
 * 提问
 * @param msg
 */
function showAsk(num_id,msg) {
    var sendHTML = '<div class="group clear right">' +
        '<img src="/static/images/me.jpg" class="portrait right" alt=""/>' +
        '<p class="message right">' + msg + '</p>' +
        '</div>';
    $(".content").append(sendHTML);
    //滚动到底部
    $(".content").scrollTop($(".content")[0].scrollHeight);
    //清空输入框
    $("#msg").val("");
    send(num_id,msg);
}

/**
 * 提问语音
 * @param id
 */
function showAskVoice(id) {
    var sendHTML = '<div class="group clear right">' +
        '<img src="images/me.jpg" class="portrait right" alt=""/>' +
        '<p class="message right" onclick="playVoice(\'' + id + '\')"><img src="images/voice.png" class="right" style="width:20px;height:20px;"></p>' +
        '</div>';
    $(".content").append(sendHTML);
    //滚动到底部
    $(".content").scrollTop($(".content")[0].scrollHeight);
}

/**
 * 播放语音
 * @param id
 */
function playVoice(id) {
    wx.playVoice({
        localId: id // 需要播放的音频的本地ID，由stopRecord接口获得
    });
}

/**
 * 发送
 * @param msg
 */
function send(num_id,msg) {
    $.ajax({
        url: "/talk/",
        type: 'POST',
        data: {"msg": msg,"num_id":num_id},
        dataType: 'json',
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            showAnswerMsg("网络连接错误哦哦哦");
        },
        success: function (result) {
            showAnswerMsg(result.data);
        }
    });
}
