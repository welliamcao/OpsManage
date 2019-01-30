function requests(method,url,data){
	var ret = '';
	$.ajax({
		async:false,
		url:url, //请求地址
		type:method,  //提交类似
       	success:function(response){
             ret = response;
        },
        error:function(data){
            ret = {};
        }
	});	
	return 	ret
}

function Percentage(num, total) {
		return (Math.round(num / total * 10000) / 100);
}	

function drawProjectChartSummary (ids,key,dataList) {
	if(dataList.length){
    	var labels = [];	
    	var data = [];
    	var trHtml = '';
    	var total = 0;
    	var colorList = ["aero","purple","green","blue","red"]
    	for (var i=0; i < dataList.length; i++){
    		data.push(dataList[i]["count"]);
    		labels.push(dataList[i][key]);
    		total = total + dataList[i]["count"]
    	}
    	init_chart_doughnut(ids,labels,data);			
	}else{
    	var labels = ["项目一", "项目二", "项目三", "项目四", "项目五"];	
		var data = [1, 2, 3, 1, 3];
		init_chart_doughnut(labels,data);  			
	}
}

function drawAllAssets(dataList) {
	$("#graph_bar").length && Morris.Bar({
        element: "graph_bar",
        data: dataList,
        xkey: "name",
        ykeys: ["count"],
        labels: ["总计"],
        barRatio: .4,
        barColors: ["#26B99A", "#34495E", "#ACADAC", "#3498DB"],
        xLabelAngle: 35,
        hideHover: "auto",
        resize: !0
    })	
}

function sparkline_sql (dataList){
	$("#sparkline_sql").sparkline(dataList, {
        type: "bar",
        height: "40",
        barWidth: 8,
        colorMap: {
            7 : "#a1a1a1"
        },
        barSpacing: 2,
        barColor: "#26B99A"
	    });			
}
function sparkline_upload(dataList){
	 $("#sparkline_upload").sparkline(dataList, {
	        type: "line",
	        width: "200",
	        height: "40",
	        lineColor: "#26B99A",
	        fillColor: "rgba(223, 223, 223, 0.57)",
	        lineWidth: 2,
	        spotColor: "#26B99A",
	        minSpotColor: "#26B99A"
	 });		
}
function sparkline_download(dataList){
	 $("#sparkline_download").sparkline(dataList, {
	        type: "bar",
	        height: "40",
	        barWidth: 8,
	        colorMap: {
	            7 : "#a1a1a1"
	        },
	        barSpacing: 2,
	        barColor: "#26B99A"
	 });
 }	

var orderStatusHtml = {
		"0":'<span class="label label-success">已通过</span>',
	    "1":'<span class="label label-danger">已拒绝</span>',
	    "2":'<span class="label label-info">审核中</span>',
	    "3":'<span class="label label-success">已部署</span> ',
	    "4":'<span class="label label-info">待授权</span>',
	    "5":'<span class="label label-success">已执行</span>',
	    "6":'<span class="label label-default">已回滚</span>',
	    "7":'<span class="label label-danger">已撤回</span>',
	    "8":'<span class="label label-warning">已授权</span>',
	    "9":'<span class="label label-danger">已失败</span>',	
	}

var orderTypeHtml = {
		"0":'<span class="label label-info">SQL更新</span>',
		"1":'<span class="label label-success">代码更新</span>',
		"2":'<span class="label label-warning">文件分发</span>',
		"3":'<span class="label label-danger">文件下载</span>'
	}

var userInfo = {
		
}

$(document).ready(function() {
	
	$(function(){
		var userList = requests("get","/api/user/")
		for (var i=0; i <userList.length; i++){
			userInfo[userList[i]["id"]] = userList[i]
		}		
	})
	
	$(function() {
		if ($("#newOrderUl").length) {
			var dataList = requests("get","/api/orders/list/")   
			console.log(dataList["results"])
            var liHmtl = ''
            var count = 0
            for (var i=0; i <dataList["results"].length; i++){
            	count += 1
            	liHmtl += '<li class="media event">' +
			              '<a class="pull-left border-green profile_thumb">' +
			                '<i class="fa fa-user green"></i>' +
			              '</a>' +
			              '<div class="media-body">' +
			                '<a class="title" href="/order/list/">工单主题：'+dataList["results"][i]["order_subject"]+'</a>' +
			                '<p><strong>申请人：'+ userInfo[dataList["results"][i]["order_user"]]["username"] +'</strong></p>' +
			                '<p> <small>工单状态：'+orderStatusHtml[dataList["results"][i]["order_status"]]+'</small>' +
			                '</p>' +
			              '</div>' +
			              '</li>'
			    if (count > 4){
			    	break
			    }
            }
			var ulHtml = '<ul class="list-unstyled top_profiles scroll-view" id="newOrderUl">' + liHmtl  + '</ul>'
			$("#newOrderUl").html(ulHtml)
		}
	})
	
	$(function() {
		$.ajax({  
	        type: "GET",  
	        url:"/api/orders/count/",  
	        async : false,  
	        error: function(response) {  
	        	$.alert({
	        	    title: 'Failed!',
	        	    content: response.responseText,
	        	});        	     
	        },  
	        success: function(response) {  
	        	orderData = response["data"]["orderCount"]
	        	floth = {
	        	        grid: {
	        	            show: !0,
	        	            aboveData: !0,
	        	            color: "#3f3f3f",
	        	            labelMargin: 10,
	        	            axisMargin: 0,
	        	            borderWidth: 0,
	        	            borderColor: null,
	        	            minBorderMargin: 5,
	        	            clickable: !0,
	        	            hoverable: !0,
	        	            autoHighlight: !0,
	        	            mouseActiveRadius: 100
	        	        },
	        	        series: {
	        	            lines: {
	        	                show: !0,
	        	                fill: !0,
	        	                lineWidth: 2,
	        	                steps: !1
	        	            },
	        	            points: {
	        	                show: !0,
	        	                radius: 4.5,
	        	                symbol: "circle",
	        	                lineWidth: 3
	        	            }
	        	        },
	        	        legend: {
	        	            position: "ne",
	        	            margin: [0, -25],
	        	            noColumns: 0,
	        	            labelBoxBorderColor: null,
	        	            labelFormatter: function(a, b) {
	        	                return a + "&nbsp;&nbsp;"
	        	            },
	        	            width: 40,
	        	            height: 1
	        	        },
	        	        colors: ["#96CA59", "#3F97EB", "#72c380", "#6f7a8a", "#f7cb38", "#5a8022", "#2c7282"],
	        	        shadowSize: 0,
	        	        tooltip: !0,
	        	        tooltipOpts: {
	        	            content: "<font color='#000000'>%x统计: %y.0</font>",
	        	            xDateFormat: "%Y/%m/%d",
	        	            shifts: {
	        	                x: -30,
	        	                y: -50
	        	            },
	        	            defaultTheme: !1
	        	        },
	        	        yaxis: {
	        	            min: 0
	        	        },
	        	        xaxis: {
	        	            mode: "time",
	        	            minTickSize: [1, "day"],
	        	            timeformat: "%Y/%m/%d",
	        	            min: orderData[0][0],
	        	            max: orderData[20][0]
	        	        }
	        	    }	        	
	            $($.plot($("#orders_plot"), [{
	                label: "工单统计",
	                data: orderData,
	                lines: {
	                    fillColor: "rgba(150, 202, 89, 0.12)"
	                },
	                points: {
	                    fillColor: "#fff"
	                }
	            }], floth))	
	            sparkline_sql(response["data"]["sqlOrder"]["dataList"])
	            sparkline_upload(response["data"]["uploadOrder"]["dataList"])
	            sparkline_download(response["data"]["downloadOrder"]["dataList"])
	            $("#order_sql_count").text(response["data"]["sqlOrder"]["all"])
	            $("#order_upload_count").text(response["data"]["uploadOrder"]["all"])
	            $("#order_download_count").text(response["data"]["downloadOrder"]["all"])
	        }  
		})		
	})

	$(function() {
		$.ajax({  
	        type: "GET",  
	        url:"/api/assets/count/",  
	        async : false,  
	        error: function(response) {  
	        	$.alert({
	        	    title: 'Failed!',
	        	    content: response,
	        	});        	     
	        },  
	        success: function(response) {  
					drawProjectChartSummary("projectCanvasDoughnut","project_env",response["data"]["appsCount"])
					drawProjectChartSummary("tagCanvasDoughnut","tags_name",response["data"]["tagCount"])
					drawProjectChartSummary("databaseCanvasDoughnut","db_env",response["data"]["dbCount"])				
					var dataList = response["data"]["allCount"]
					drawAllAssets(dataList)
					for (var i=0; i <dataList.length; i++){
	            		switch (dataList[i]["name"])
	            		{
		            		case "总资产":
		            			$("#totalAssets").text(dataList[i]["count"])
		            			break;
		            		case "总工单数":
		            			$("#totalOrders").text(dataList[i]["count"])
		            			break;
		            		case "数据库":
		            			$("#totalDbs").text(dataList[i]["count"])
			            		break;
		            		case "代码部署":
		            			$("#totalApps").text(dataList[i]["count"])
			            		break;
	            		}					
					}
	        }  
		})
	})
})