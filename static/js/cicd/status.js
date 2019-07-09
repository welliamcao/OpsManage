function getDateTime(seconds,fmt){
    var nowDate = new Date(new Date().getTime() - 1 * seconds * 1000);   
    var year = nowDate.getFullYear();  
    var month = nowDate.getMonth() + 1 < 10 ? "0" + (nowDate.getMonth() + 1) : nowDate.getMonth() + 1;  
    var date = nowDate.getDate() < 10 ? "0" + nowDate.getDate() : nowDate.getDate();  
    var hour = nowDate.getHours()< 10 ? "0" + nowDate.getHours() : nowDate.getHours();  
    var minute = nowDate.getMinutes()< 10 ? "0" + nowDate.getMinutes() : nowDate.getMinutes();  
    var second = nowDate.getSeconds()< 10 ? "0" + nowDate.getSeconds() : nowDate.getSeconds(); 
	switch (fmt)
	{
		case 'yyyy-MM-dd':
			return year + "-" + month + "-" + date; 
		case 'yyyy/MM/dd HH:mm:SS':
			return year + "/" + month + "/" + date+" "+hour+":"+minute+":"+second;  
		case 'yyyyMMddHHmm':
			return year.toString() +  month.toString()  + date.toString() + hour.toString() +minute.toString() 
		case 'yyyy-MM-dd HH:mm':
			return year + "-" + month + "-" + date+" "+hour+":"+minute 
		case 'yyyy-MM-dd HH:mm:SS':
			return year + "-" + month + "-" + date+" "+hour+":"+minute+":"+second;  			            	
	}    
    
}

var downLoadFile = function (options){
    var config = $.extend(true, { method: 'post' }, options);
    var $iframe = $('<iframe id="down-file-iframe"/>');
    var $form = $("<form target='down-file-iframe' method=" + config.method + " />");
    $form.attr('action', config.url);
    for (var key in config.data) {
        $form.append('<input type="hidden" name="' + key + '" value="' + config.data[key] +  '"/>');
    }
    $form.append('<input type="hidden" name="csrfmiddlewaretoken" value="'+ $("input[name='csrfmiddlewaretoken']").val() +'">');
    $iframe.append($form);
    $(document.body).append($iframe);
    $form[0].submit();
    $iframe.remove();
}	

function downLoadPackage(obj,task_id){
	$("button[name='download_button']").attr("disabled",true);
    var url = '/apps/manage/';	
    var data = {
			'id':get_url_param("id"),
			'tasks_id':task_id,
			'type':'download_package'
     };
    downLoadFile({ //调用下载方法
	        	url:url,data:data
	        	}); 
    $("button[name='download_button']").attr("disabled",false);
}	

function createRandom(num , from , to)
{
    var arr=[];
    var json={};
    while(arr.length<num)
    {
        var ranNum=Math.ceil(Math.random()*(to-from))+from;
        if(!json[ranNum])
        {
            json[ranNum]=1;
            arr.push(ranNum);
        }
         
    }
    return arr;
}

function get_url_param(name) {
	 var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
	 var r = window.location.search.substr(1).match(reg);
	 if (r != null) return unescape(r[2]); return null; 
}

function draw_cpu_line(dataList){
	$("#draw_line_cpu").empty()
	$("#draw_line_cpu").length && (Morris.Line({
        element: "draw_line_cpu",
        xkey: "dtime",
        ykeys: ["value"],
        labels: ["Value"],
        hideHover: "auto",
        parseTime: false,
        lineColors: ["#26B99A", "#34495E", "#ACADAC", "#3498DB"],
        data: dataList,
        resize: !0
    }), $MENU_TOGGLE.on("click",
    function() {
        $(window).resize()
    }))
}

function draw_qps_line(dataList){
	$("#draw_line_qps").empty()
	$("#draw_line_qps").length && (Morris.Line({
        element: "draw_line_qps",
        xkey: "dtime",
        ykeys: ["value"],
        labels: ["Value"],
        hideHover: "auto",
        parseTime: false,
        lineColors: ["#26B99A", "#34495E", "#ACADAC", "#3498DB"],
        data: dataList,
        resize: !0
    }), $MENU_TOGGLE.on("click",
    function() {
        $(window).resize()
    }))
}

function draw_50x_line(dataList){
	$("#draw_line_50x").empty()
	$("#draw_line_50x").length && (Morris.Line({
        element: "draw_line_50x",
        xkey: "dtime",
        ykeys: ["value"],
        labels: ["Value"],
        hideHover: "auto",
        parseTime: false,
        lineColors: ["#26B99A", "#34495E", "#ACADAC", "#3498DB"],
        data: dataList,
        resize: !0
    }), $MENU_TOGGLE.on("click",
    function() {
        $(window).resize()
    }))
}

function draw_taffic_line(dataList){
	$("#draw_line_taffic").empty()
	$("#draw_line_taffic").length && (Morris.Area(
		{
			parseTime: false,
	        element: "draw_line_taffic",
	        data: dataList,
	        xkey: "dtime",
	        ykeys: ["in", "out"],
	        lineColors: ["#26B99A", "#34495E"],
	        labels: ["in", "out"],
	        pointSize: 2,
	        hideHover: "auto",
	        resize: !0
	    }
    ), $MENU_TOGGLE.on("click",
    function() {
        $(window).resize()
    }))
}

function draw_disk_line(dataList){
	$("#draw_line_disk").empty()
	$("#draw_line_disk").length && (Morris.Area(
		{
			parseTime: false,
	        element: "draw_line_disk",
	        data: dataList,
	        xkey: "dtime",
	        ykeys: ["read", "write"],
	        lineColors: ["#26B99A", "#34495E"],
	        labels: ["in", "out"],
	        pointSize: 2,
	        hideHover: "auto",
	        resize: !0
	    }
    ), $MENU_TOGGLE.on("click",
    function() {
        $(window).resize()
    }))
}

function draw_mem_line(dataList){
	$("#draw_line_mem").empty()
	$("#draw_line_mem").length && (Morris.Area({
        element: "draw_line_mem",
        xkey: "dtime",
        ykeys: ["value"],
        labels: ["Value"],
        hideHover: "auto",
        parseTime: false,
        lineColors: ["#26B99A", "#34495E", "#ACADAC", "#3498DB"],
        data: dataList,
        resize: !0
    }), $MENU_TOGGLE.on("click",
    function() {
        $(window).resize()
    }))
}


function draw_monitor_line(key,id,startTime,endtime){
	$.ajax({  
        cache: true,  
        type: "get",  
        url:'/api/monitor/apps/'+ id +'/?type='+key+'&startTime='+startTime+'&endtime=' + endtime,
        success: function(data) {  
        	switch (key)
        	{
        		case 'cpu':
        			draw_cpu_line(data)
        			break;
        		case 'mem':
        			draw_mem_line(data)
        			break; 
        		case 'disk':
        			draw_disk_line(data) 
        			break;
        		case 'taffic':
        			draw_taffic_line(data) 
        			break;
        		case 'qps':
        			draw_qps_line(data) 
        			break; 
        		case 'http_error':
        			draw_50x_line(data) 
        			break;           			
        	}         	
        	
        }  
	}); 
}

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

var language =  {
	"sProcessing" : "处理中...",
	"sLengthMenu" : "显示 _MENU_ 项结果",
	"sZeroRecords" : "没有匹配结果",
	"sInfo" : "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
	"sInfoEmpty" : "显示第 0 至 0 项结果，共 0 项",
	"sInfoFiltered" : "(由 _MAX_ 项结果过滤)",
	"sInfoPostFix" : "",
	"sSearch" : "搜索: ",
	"sUrl" : "",
	"sEmptyTable" : "表中数据为空",
	"sLoadingRecords" : "载入中...",
	"sInfoThousands" : ",",
	"oPaginate" : {
		"sFirst" : "首页",
		"sPrevious" : "上页",
		"sNext" : "下页",
		"sLast" : "末页"
	},
	"oAria" : {
		"sSortAscending" : ": 以升序排列此列",
		"sSortDescending" : ": 以降序排列此列"
	}
}


function InitDataTable(tableId,url,columns,columnDefs){
  var data = requests('get',url)
  oOverviewTable =$('#'+tableId).dataTable(
		  {
	    		"bScrollCollapse": false, 				
	    	    "bRetrieve": true,			
	    		"destroy": true, 
	    		"data":	data['results'],
	    		"columns": columns,
	    		"columnDefs" :columnDefs,			  
	    		"language" : language,
	    		"order": [[ 0, "ase" ]],
	    		"autoWidth": false	    			
	    	});
  if (data['next']){
	  $("button[name='page_next']").attr("disabled", false).val(data['next']);	
  }else{
	  $("button[name='page_next']").attr("disabled", true).val();
  }
  if (data['previous']){
	  $("button[name='page_previous']").attr("disabled", false).val(data['next']);	
  }else{
	  $("button[name='page_previous']").attr("disabled", true).val();
  }
}

function RefreshTable(tableId, urlData)
{
  $.getJSON(urlData, null, function( dataList )
  {
    table = $(tableId).dataTable();
    oSettings = table.fnSettings();
    
    table.fnClearTable(this);

    for (var i=0; i<dataList['results'].length; i++)
    {
      table.oApi._fnAddData(oSettings, dataList['results'][i]);
    }

    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
    table.fnDraw();
    
    if (dataList['next']){
  	  $("button[name='page_next']").attr("disabled", false).val(dataList['next']);	
    }else{
  	  $("button[name='page_next']").attr("disabled", true).val();
    }
    if (dataList['previous']){
  	  $("button[name='page_previous']").attr("disabled", false).val(dataList['previous']);	
    }else{
  	  $("button[name='page_previous']").attr("disabled", true).val();
    }    
  });
}

function AutoReload(tableId,url)
{
  RefreshTable('#'+tableId, url);
  setTimeout(function(){AutoReload(url);}, 30000);
}

$(document).ready(function() {
	var randromChat = makeRandomId()
	if ($("#sparkline_line_cpu").length){
		$("#sparkline_line_cpu").sparkline(createRandom(12,1,90), {
		    type: 'line',
		    width: '300px',
	        lineColor: "#26B99A",
	        fillColor: "#ffffff",
	        spotColor: "#34495E",
	        minSpotColor: "#34495E"	    
		    });			
	}
	if ($("#sparkline_area_bitin").length){
		 $("#sparkline_area_bitin").sparkline(createRandom(12,10,200), {
		        type: "line",
		        lineColor: "#26B99A",
		        fillColor: "#26B99A",
		        spotColor: "#4578a0",
		        minSpotColor: "#728fb2",
		        maxSpotColor: "#6d93c4",
		        highlightSpotColor: "#ef5179",
		        highlightLineColor: "#8ba8bf",
		        spotRadius: 2.5,
		        width: '300px'
		 });		
	}
	if ($("#sparkline_area_bitout").length){
		 $("#sparkline_area_bitout").sparkline(createRandom(12,10,200), {
		        type: "line",
		        lineColor: "#26B99A",
		        fillColor: "#26B99A",
		        spotColor: "#4578a0",
		        minSpotColor: "#728fb2",
		        maxSpotColor: "#6d93c4",
		        highlightSpotColor: "#ef5179",
		        highlightLineColor: "#8ba8bf",
		        spotRadius: 2.5,
		        width: '300px'
		 });
	 }
	 if ($("#sparkline_area_mem").length){
		 $("#sparkline_area_mem").sparkline(createRandom(12,10,200), {
		        type: "line",
		        lineColor: "#26B99A",
		        fillColor: "#26B99A",
		        spotColor: "#4578a0",
		        minSpotColor: "#728fb2",
		        maxSpotColor: "#6d93c4",
		        highlightSpotColor: "#ef5179",
		        highlightLineColor: "#8ba8bf",
		        spotRadius: 2.5,
		        width: '300px'
		 });			 
	 }
 
	 
	 $("#project_version").change(function(){
		 desc = $("#project_version option:selected").text().split(" - ")
		 if (desc.length > 1){
			 $("#desc").val(desc[1])
		 }else{
			 $("#desc").val(desc[0])
		 }
		 $("#btn-deploy-project").attr("disabled",false);
	 });	
	 
	 
	 $("#git_project_branch").change(function(){
		 desc = $("#git_project_branch option:selected").text().split(" - ")
		 if (desc.length > 1){
			 $("#desc").val(desc[1])
		 }else{
			 $("#desc").val(desc[0])
		 }
		 $("#btn-deploy-project").attr("disabled",false);
	 });	 
	 
	 $("#branch_choice").change(function(){
		   var obj = document.getElementById("branch_choice"); 
		   var index = obj.selectedIndex;
		   var value = obj.options[index].value; 
		   obj.options[index].selected = true;
		   $('#project_version').html("");
		   $("#btn-deploy-project").attr("disabled",true);
		   if (value.length > 0 ){
				$.ajax({
					  type: 'get',
					  url: '/apps/manage/?type=query_repo&name='+ value +'&id=' + get_url_param('id'),
				      success:function(response){	
			                if (response["code"]=="200"){ 
			        			var htmlStr = '<select class="form-control" name="project_version" id="project_version"  required><option selected="selected" value="" name="order_comid" >请选择版本</option>';
			        			for (x in response["data"]){
									htmlStr += '<option value="'+ response["data"][x]['comid'] + '"name="order_comid">' + response["data"][x]['ver'] + ' - ' + response["data"][x]['desc'] + ' - ' + response["data"][x]['user'] +'</option>';																
								};
								htmlStr += '</select>'
								$('#project_version').html(htmlStr);
			                }
					},
		            error:function(response){
    		           	new PNotify({
  		                   title: 'Ops Failed!',
  		                   text: response.responseText,
  		                   type: 'error',
  		                   styling: 'bootstrap3'
  		               });
		            },							  
					})		   	   
		   }	 
	 });
	 
	 $('button[name="refresh-repo-branch"]').click(function(){
		 var btnObj = $(this);
		 btnObj.attr('disabled',true);
		 $.ajax({
			  type: 'get',
			  url: '/apps/manage/?type=refresh_branch&id=' + get_url_param('id'),
		      success:function(response){	
	                if (response["code"]=="200"){ 
	        			var htmlStr = '<select class="selectpicker form-control" name="project_branch"  id="branch_choice"><option selected="selected" value="" name="project_branch" >请选择分支</option>';
	        			for (x in response["data"]){
							htmlStr += '<option value="'+ response["data"][x] + '"name="project_branch">' + response["data"][x] +'</option>';																
						};
						htmlStr += '</select>'
						$('#branch_choice').html(htmlStr);
						$('.selectpicker').selectpicker('refresh');	
	                }
	                btnObj.removeAttr('disabled');
			},
            error:function(response){
	           	new PNotify({
	                   title: 'Ops Failed!',
	                   text: response.responseText,
	                   type: 'error',
	                   styling: 'bootstrap3'
	               });
	           	btnObj.removeAttr('disabled');
            },							  
		})	
	 });	 
	 
	 $('button[name="refresh-repo-commit"]').click(function(){
		 var btnObj = $(this);
		 btnObj.attr('disabled',true);
		 $.ajax({
			  type: 'get',
			  url: '/apps/manage/?type=refresh_commit&id=' + get_url_param('id'),
		      success:function(response){	
	                if (response["code"]=="200"){ 
	        			var htmlStr = '<select class="selectpicker form-control" name="project_branch"  id="branch_choice"><option selected="selected" value="" name="project_branch" >请选择分支</option>';
	        			for (x in response["data"]){
							htmlStr += '<option value="'+ response["data"][x] + '"name="project_branch">' + response["data"][x] +'</option>';																
						};
						htmlStr += '</select>'
						$('#branch_choice').html(htmlStr);
						$('.selectpicker').selectpicker('refresh');	
	                }
	                btnObj.removeAttr('disabled');
			},
            error:function(response){
	           	new PNotify({
	                   title: 'Ops Failed!',
	                   text: response.responseText,
	                   type: 'error',
	                   styling: 'bootstrap3'
	               });
	           	btnObj.removeAttr('disabled');
            },							  
		})		   	   
	 });	 
 
	    $('#btn-deploy-project').on('click',function(){
    		var btnObj = $(this);   		
    		var is_confirm = true;
    		btnObj.attr('disabled',true);
    		$("div[name='deploy_result']").empty()
			$("#pre_deploy_block").hide()
		    $("#post_deploy_block").hide()
		    $("#package_deploy_block").hide()
		    $("#pre_release_block").hide()
		    $("#release_block").hide()
		    $("#post_release_block").hide()	     		
    		var servers = new Array();
			$("#deploy_server option:selected").each(function(){
				servers.push($(this).val());
	        });   
			if (servers.length==0){
	        	new PNotify({
	                title: 'Warning!',
	                text: '请注意主机不能为空~',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
				btnObj.removeAttr('disabled');
				return false;
			}  
    	    let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    	    let websocket = new WebSocket(ws_scheme + '://' + window.location.host + "/apps/deploy/" + $(this).val() + '/' + randromChat + '/');
    	    websocket.onopen = function () {
    	    	var data = {
    				"tag": $('#git_project_branch option:selected').val(),
    	    		"commit_id" :  $("#project_version").val(),
    	    		"branch" :  $('#branch_choice option:selected').val(), 
    	    		"id" :  $("#project_id").val(), 
    	    		"server":servers,
    	    		"action":"deploy"
    	    	}
    	    	websocket.send(JSON.stringify(data));
    	    };

    	    websocket.onmessage = function (event) {
	    		result = JSON.parse(event.data)	 
        		$("#"+result['progress']+"_block").show()		            		
        		$("#"+result['progress']+"_ctime").text(result["ctime"])
        		$("#"+result['progress']+"_user").text(result["user"])
        		if (result["status"] == 'failed'){
            		$("#"+result['progress']+"_block").find("i").css({
						  "color":"red",
						  "class":""
					}).attr("class", "fa fa-times-circle");		            			
        		}		            		
        		$("#"+result['progress']+"_result").append("<p>"+result["msg"]+"</p>"); 
        	   if (result["status"] == "done" && result["progress"] == "summary"){
        			websocket.close();
        	   }
        	   else if(result["status"] == "error"){
        			$.alert({
        			    title: '代码部署失败',
        			    content: result["msg"],
        			    type: 'red'		    
        			});        		   
        	   }
    	   };

    	   websocket.onerror = function(event) {
            	new PNotify({
		              title: 'Warning!',
		              text: event.data,
		              type: 'warning',
		              styling: 'bootstrap3'
		        });    	    	
    	    	websocket.close();
    	    };    
    	    
    	    websocket.onclose = function () {
    	    	btnObj.removeAttr('disabled');
    	    }		
    	    
	        // 关闭窗口时弹出确认提示
	        $(window).bind('beforeunload', function () {
	            // 只有在标识变量is_confirm不为false时，才弹出确认提示
	            if (window.is_confirm !== false) {
	                return "您可能有数据没有保存";
	            }
	        });
	        // mouseleave mouseover事件也可以注册在body、外层容器等元素上
	        $(window).bind('mouseover mouseleave', function (event) {
	            is_confirm = event.type == 'mouseleave';
	        });
    	    
	    })	 
	    
//	    (function () {
//	        // 关闭窗口时弹出确认提示
//	        $(window).bind('beforeunload', function () {
//	            // 只有在标识变量is_confirm不为false时，才弹出确认提示
//	            if (window.is_confirm !== false) {
//	                return "您可能有数据没有保存";
//	            }
//	        });
//	        // mouseleave mouseover事件也可以注册在body、外层容器等元素上
//	        $(window).bind('mouseover mouseleave', function (event) {
//	            is_confirm = event.type == 'mouseleave';
//	        });
//	    })();	    
	    
	$("#appsperformance").on("click", function(){
		var startTime = getDateTime(1800,'yyyyMMddHHmm') 
		var endtime = getDateTime(1,'yyyyMMddHHmm') 
		draw_monitor_line('cpu',get_url_param('id'),startTime,endtime)
		draw_monitor_line('mem',get_url_param('id'),startTime,endtime)
		draw_monitor_line('disk',get_url_param('id'),startTime,endtime)
		draw_monitor_line('taffic',get_url_param('id'),startTime,endtime)
		draw_monitor_line('qps',get_url_param('id'),startTime,endtime)
		draw_monitor_line('http_error',get_url_param('id'),startTime,endtime)		 
	})
	
	$("#deploylog").on("click", function(){

	    if ($("#deployResultList").length) {
	    	
	    	function makeDeployResultList(){
			    var columns = [
			                    {"data": "id"},
			                    {"data": "project_env"},
				                {"data": "project_name"},
				                {"data": "type","sClass": "text-center"},
				                {"data": "username"},		
				                {"data": "package"},	
				                {"data": "git_version","defaultContent": ''},	
				                {"data": "create_time","sClass": "text-center"},			                
				                {"data": "status","sClass": "text-center"},
				                
				               ]
			    var columnDefs = [	
									{
										targets: [1],
										render: function(data, type, row, meta) {
											if(row.project_env=='sit'){
												var env = '<code>测试环境</code>'
											}else if(row.project_env=='uat'){
												var env = '<code>正式环境</code>'
											}else{
												var env = '<code>灰度环境</code>'
											}
									        return env
										},
									},
									{
										targets: [5],
										render: function(data, type, row, meta) {
											if(row.package == "未知" ){
												return row.package
											}else{
												return '<p onclick="downLoadPackage(this,\'' + row.id + '\',\''  +'\')"><u><span color: #0000ff;>'+row.package+'</span></u></p>'
												//return '<button type="button" name="download_button" class="btn btn-xs btn-default" onclick="downLoadPackage(this,\'' + row.id + '\',\''  +'\')"><abbr title="'+ row.package +'"><i class="fa  fa-cloud-download"></i></button>';
											}
										},
									},									
									{
										targets: [8],
										render: function(data, type, row, meta) {
											if(row.status=='已部署'){
												var status = '<span class="label label-success">已部署</span>'
											}else if (row.status=='进行中'){
												var status = '<span class="label label-info">'+ row.status +'</span>'
											}else{
												var status = '<span class="label label-danger">'+ row.status +'</span>'
											}
									        return status
										},
									},
									{
										targets: [3],
										render: function(data, type, row, meta) {
											if(row.type=='deploy'){
												var env = '<span class="label label-info"><strong>部署</strong></span>'
											}else{
												var env = '<span class="label label-warning"><strong>回滚</strong></span>'
											}
									        return env
										},
									},								
		    	    		        {
			    	    				targets: [9],
			    	    				render: function(data, type, row, meta) {
											if(row.type=='deploy' && row.status=='已部署'){
												var rollback = '<button type="button" name="btn-task-rollback" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify" data-toggle="modal" data-target=".bs-example-modal-rollback"><span class="fa fa-recycle" aria-hidden="true"></span>' +	
				    	                           			   '</button>' 
											}else{
												var rollback = '<button type="button" name="btn-task-rollback" class="btn btn-default"  aria-label="Justify" disabled><span class="fa fa-recycle" aria-hidden="true"></span>' +	
	 	                           			   				   '</button>'
											}		    	    					
			    	                        return '<div class="btn-group  btn-group-xs">' +	
				    	                           '<button type="button" name="btn-task-view" value="'+ row.task_id +'" class="btn btn-default"  aria-label="Justify" data-toggle="modal" data-target=".bs-example-modal-info"><span class="fa fa-search-plus" aria-hidden="true"></span>' +	
				    	                           '</button>' + rollback +		                				                            		                            			                          
				    	                           '<button type="button" name="btn-task-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span>' +	
				    	                           '</button>' +			                            
				    	                           '</div>';
			    	    				},
			    	    				"className": "text-center",
		    	    		        },
		    	    		      ]
			    
			    InitDataTable('deployResultList','/api/apps/logs/?pid='+get_url_param('id'),columns,columnDefs);
			    //每隔30秒刷新table
			    //setTimeout(function(){AutoReload('deployResultList','/api/apps/logs/?pid='+get_url_param('id'));}, 30000);    		
	    	}
	    	makeDeployResultList()
		    
		}			
		
	})
    
    var rollback_content = ""
    
	$('#deployResultList tbody').on('click','button[name="btn-task-rollback"]',function(){
		rollback_content = $(this).parent().parent().parent().find("td").eq(6).text()
		$("#rollbackTitle").html('<h4 class="modal-title" id="rollbackTitle">代码回滚   <code>'+rollback_content+'</code></h4>')
		$("#btn-rollback-project").val($(this).val())
	});	    
  
	
	    $('#btn-rollback-project').on('click',function(){
    		var btnObj = $(this);   		
    		var is_confirm = true;
    		btnObj.attr('disabled',true);
			$("#rollback_code_block_rb").hide()
			$("#rsync_code_block_rb").hide()
			$("#cmd_code_block_rb").hide()	
			$("div[name='deploy_result']").empty()	     		
    	    let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    	    let websocket = new WebSocket(ws_scheme + '://' + window.location.host + "/apps/deploy/" +  $("#project_id").val() + '/' + randromChat + '/');
    	    websocket.onopen = function () {
    	    	var data = {
    				"task_ids": btnObj.val(),
    	    		"action":"rollback"
    	    	}
    	    	websocket.send(JSON.stringify(data));
    	    };

    	    websocket.onmessage = function (event) {
	    		result = JSON.parse(event.data)	 
        		$("#"+result['progress']+"_block_rb").show()	
        		console.log("#"+result['progress']+"_block_rb")
        		$("#"+result['progress']+"_ctime_rb").text(result["ctime"])
        		$("#"+result['progress']+"_user_rb").text(result["user"])
        		if (result["status"] == 'failed'){
            		$("#"+result['progress']+"_block_rb").find("i").css({
						  "color":"red",
						  "class":""
					}).attr("class", "fa fa-times-circle");		            			
        		}		            		
        		$("#"+result['progress']+"_result_rb").append("<p>"+result["msg"]+"</p>"); 
        	   if (result["status"] == "done" && result["progress"] == "summary"){
        			websocket.close();
        	   }
        	   else if(result["status"] == "error"){
        			$.alert({
        			    title: '代码部署失败',
        			    content: result["msg"],
        			    type: 'red'		    
        			});        		   
        	   }
    	   };

    	   websocket.onerror = function(event) {
            	new PNotify({
		              title: 'Warning!',
		              text: event.data,
		              type: 'warning',
		              styling: 'bootstrap3'
		        });    	    	
    	    	websocket.close();
    	    };    
    	    
    	    websocket.onclose = function () {
    	    	btnObj.removeAttr('disabled');
    	    }		  	    
    	    
	    })		
	
	
	
	$('#deployResultList tbody').on('click','button[name="btn-task-view"]',function(){
		$(this).attr('disabled',true);
    	var vIds = $(this).val();
	    $("div[name='deploy_record_result']").empty()
		$("#pre_deploy_record_block").hide()
		$("#post_deploy_record_block").hide()
	    $("#package_deploy_record_block").hide()
	    $("#pre_release_record_block").hide()
	    $("#release_record_block").hide()
	    $("#post_release_record_block").hide()	
	    var username = $(this).parent().parent().parent().find("td").eq(4).text()
    	$.ajax({  
            cache: true,  
            type: "GET",  
            url:"/api/apps/logs/detail/"+ vIds +"/",  
            async: false,  
            error: function(response) {  
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 
            },  
            success: function(response) {   	
            	if (Object.keys(response).length > 0){
        			for (var i = 0; i < response.length; ++i) {
        				console.log("#"+response[i]['key']+"_record_block")
        				$("#"+response[i]['key']+"_record_block").show()
	            		$("#"+response[i]['key']+"_record_ctime").text(response[i]["create_time"])
	            		$("#"+response[i]['key']+"_record_user").text(username)
	            		$("#"+response[i]['key']+"_record_result").append("<p>"+response[i]["msg"]+"</p>");
	            		if (response[i]["status"] == 'failed'){
		            		$("#"+response[i]['key']+"_record_block").find("i").css({
								  "color":"red",
								  "class":""
							}).attr("class", "fa fa-times-circle");		            			
	            		}	        				
        			}
            	}
            }  
    	});    	
		$(this).attr('disabled',false);
	});	    
    
	
	$('#deployResultList tbody').on('click','button[name="btn-task-delete"]',function(){
		$(this).attr('disabled',true);
    	var vIds = $(this).val();
	    var text = $(this).parent().parent().parent().find("td").eq(6).text()
		$.confirm({
		    title: '删除确认',
		    content: text,
		    type: 'red',
		    buttons: {
		             删除: function () {
		    	$.ajax({  
		            cache: true,  
		            type: "DELETE",  
		            url:"/api/apps/log/"+ vIds +"/",
		            error: function(response) {  
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: "删除失败",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                });     
		            },  
		            success: function(response) {  
		            	new PNotify({
		                    title: 'Success!',
		                    text: "删除成功",
		                    type: 'success',
		                    styling: 'bootstrap3'
		                });	
		            	RefreshTable('#deployResultList','/api/apps/logs/?pid='+get_url_param('id'));
		            }  
		    	});
		        },
		        取消: function () {
		            return true;			            
		        },			        
		    }
		});	    
	    
		$(this).attr('disabled',false);
	});	
	
	
    $("button[name^='page_']").on("click", function(){
      	var url = $(this).val();
      	$(this).attr("disabled",true);
      	if (url.length){
      		RefreshTable('#deployResultList', url);
      	}      	
    	$(this).attr('disabled',false);
      }); 		
	
	$("#optimize").on("click", function(){
    	$.ajax({  
            cache: true,  
            type: "GET",  
            url:"/apps/config/?type=info&id="+ get_url_param('id') ,  
            async: false,  
            error: function(response) {  
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 
            },  
            success: function(response) {   	
            	if (response["code"]=="200"){
            		var serverSelect = '<select  class="selectpicker form-control"  data-size="10" data-selected-text-format="count > 5" data-live-search="true" data-width="100%"   autocomplete="off"  class="form-control"   autocomplete="off" name="server" id="server"  required>'
            		var serverSelectOption = ''	
            		var logpathSelectOption = ''	
            		var logList = []	           		
            		for (var i = 0; i < response["data"]["number"].length; ++i) {
            			serverSelectOption += '<option name="server" value="'+ response["data"]["number"][i]["id"] +'">'+ response["data"]["number"][i]["ip"]  +'</option>'
            			var logsPath = response["data"]["project_logpath"].split(";")
            			for(var x = 0; x < logsPath.length; ++x){
            				if(logList.indexOf(logsPath[x]) == -1){
            					logList.push(logsPath[x])
            					logpathSelectOption += '<option name="server" value="'+ logsPath[x] +'">'+ logsPath[x]  +'</option>'
            				}
            			}
            		}
            		serverSelect += serverSelectOption + '</select>'
            		$("#server").html(serverSelect)
            		var logpathSelect = '<select  class="selectpicker form-control"  data-size="10" data-selected-text-format="count > 5" data-live-search="true" data-width="100%"   autocomplete="off"  class="form-control"   autocomplete="off" name="server" id="logpath"  required>'
            		logpathSelect += logpathSelectOption + '</select>'
            		$("#logpath").html(logpathSelect)
            		$('.selectpicker').selectpicker('refresh');	
            	}
            }  
    	}); 		 
	})    
	
    $("#btn-deploy-logview").on('click', function() {
    	var btnObj = $(this);
    	btnObj.attr('disabled',true);
		$.ajax({
			dataType: "JSON",
			url:"/apps/manage/" ,  
			type:"POST",  //提交类似
			data:$("#deployRunLogs").serialize(),
            error: function(response) {  
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 
            	btnObj.attr('disabled',false);
            },			
			success:function(response){
				if (response["code"]=="200"){
					$("#viewLogsResult").html('<pre>'+response["data"][0]["msg"]+'</pre>')
				}else{
					$.confirm({
					    title: '部署失败',
					    content: response["msg"],
					    type: 'red',
					    typeAnimated: true,
					    buttons: {
					        close: function () {
					        }
					    }
					});					
				}
				btnObj.attr('disabled',false);	
			}					
		});
		
    });	
	
    $("#member").on('click', function() {
		$.ajax({
			dataType: "JSON",
			url:"/apps/config/?type=info&id="+get_url_param('id'),  
			type:"GET",  //提交类似
			async:false,
            error: function(response) {  
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 
            	btnObj.attr('disabled',false);
            },			
			success:function(response){
			    var columns = [
			                    {"data": "id"},
			                    {"data": "username"},
				                {"data": "email"},
				                {"data": "role","sClass": "text-center"},				                
				               ]
			    var columnDefs = [	
									{
										targets: [1],
										render: function(data, type, row, meta) {
									        return '<span title="'+ row.user +'">'+ row.username +'</span>'
										},
									},			                      
									{
										targets: [3],
										render: function(data, type, row, meta) {
											if(row.role=='deploy'){
												var env = '<span class="label label-info"><strong>开发人员</strong></span>'
											}else{
												var env = '<span class="label label-warning"><strong>管理人员</strong></span>'
											}
									        return env
										},
									},								
		    	    		        {
			    	    				targets: [4],
			    	    				render: function(data, type, row, meta) {		    	    					
			    	                        return '<div class="btn-group  btn-group-xs">' +	
				    	                           '<button type="button" name="btn-role-edit" value="'+ row.id +'" class="btn btn-default"  aria-label="Justify"><span class="fa fa-edit" aria-hidden="true"></span>' +	
				    	                           '</button>' +                 				                            		                            			                          
				    	                           '<button type="button" name="btn-role-delete" value="'+ row.id +'" class="btn btn-default" aria-label="Justify"><span class="fa fa-trash" aria-hidden="true"></span>' +	
				    	                           '</button>' +			                            
				    	                           '</div>';
			    	    				},
			    	    				"className": "text-center",
		    	    		        },
		    	    		      ]				
	            $("#deployRolesList").length && $("#deployRolesList").DataTable({
	                dom: "Bfrtip",
	                buttons: [{
	                    text: '<span class="fa fa-plus"></span>',
	                    className: "btn-xs",
	                    action: function ( e, dt, node, config ) {
	                    	makeAppsRole()
	                    }
	                }],	
		    		"bScrollCollapse": false, 				
		    	    "bRetrieve": true,			
		    		"destroy": true, 
		    		"data":	response["data"]["roles"],
		    		"columns": columns,
		    		"columnDefs" :columnDefs,			  
		    		"language" : language,
		    		"order": [[ 0, "ase" ]],
		    		"autoWidth": false	 		    		
	            })					
			}					
		});    	
    });	
    
    function RefreshDeployRolesTable(tableId, urlData)
    {
      $.getJSON(urlData, null, function( dataList )
      {
        table = $(tableId).dataTable();
        oSettings = table.fnSettings();
        
        table.fnClearTable(this);

        for (var i=0; i<dataList["data"]["roles"].length; i++)
        {
          table.oApi._fnAddData(oSettings, dataList["data"]["roles"][i]);
        }

        oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
        table.fnDraw();
           
      });
    }    
    
    function makeAppsRole(){
		$.ajax({
			dataType: "JSON",
			url:"/api/user/" ,  
			type:"get",  //提交类似
			async:false,
            error: function(response) {  
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 
            	btnObj.attr('disabled',false);
            },			
			success:function(response){
        		var roleSelect = '<select  class="selectpicker form-control"  data-size="10" data-selected-text-format="count > 5" data-live-search="true" data-width="100%"   autocomplete="off"  class="form-control"   autocomplete="off" name="user" id="apps_role"  required>'
        		var roleSelectOption = ''	           		
        		for (var i = 0; i < response.length; ++i) {
        			roleSelectOption += '<option name="user" value="'+ response[i]["id"] +'">'+ response[i]["username"]  +'</option>'
        		}
        		roleSelect += roleSelectOption + '</select>'
        		$("#apps_role").html(roleSelect)
        		$('.selectpicker').selectpicker('refresh');	
				$(".bs-example-modal-role").modal('show');
			}					
		});    	
    }
    
    $("#btn-role-project").on('click', function() {
    	var btnObj = $(this);
		$.ajax({
			dataType: "JSON",
			url:"/api/apps/roles/" ,  
			type:"POST",  //提交类似
			data:$("#addAppsRole").serialize(),
            error: function(response) {  
            	new PNotify({
                    title: 'Ops Failed!',
                    text: response.responseText,
                    type: 'error',
                    styling: 'bootstrap3'
                }); 
            	btnObj.attr('disabled',false);
            },			
			success:function(response){
            	new PNotify({
                    title: 'Success!',
                    text: "添加成功",
                    type: 'success',
                    styling: 'bootstrap3'
                });	
            	RefreshDeployRolesTable("#deployRolesList","/apps/config/?type=info&id="+get_url_param('id'))
			}					
		});
    });  
    
	$('#deployRolesList tbody').on('click','button[name="btn-role-delete"]',function(){
		$(this).attr('disabled',true);
    	var vIds = $(this).val();
	    var username = $(this).parent().parent().parent().find("td").eq(1).text()
	    var roles = $(this).parent().parent().parent().find("td").eq(3).text()
		$.confirm({
		    title: '删除确认',
		    content: "删除【<code>"+ username +"</code>】<strong>"+roles+"</strong>角色？",
		    type: 'red',
		    buttons: {
		             删除: function () {
		    	$.ajax({  
		            cache: true,  
		            type: "DELETE",  
		            url:"/api/apps/roles/"+ vIds +"/",
		            error: function(response) {  
		            	new PNotify({
		                    title: 'Ops Failed!',
		                    text: "删除失败",
		                    type: 'error',
		                    styling: 'bootstrap3'
		                });     
		            },  
		            success: function(response) {  
		            	new PNotify({
		                    title: 'Success!',
		                    text: "删除成功",
		                    type: 'success',
		                    styling: 'bootstrap3'
		                });	
		            	RefreshDeployRolesTable("#deployRolesList","/apps/config/?type=info&id="+get_url_param('id'))
		            }  
		    	});
		        },
		        取消: function () {
		            return true;			            
		        },			        
		    }
		});	    
	    
		$(this).attr('disabled',false);
	});
    
	$('#deployRolesList tbody').on('click','button[name="btn-role-edit"]',function(){
		$(this).attr('disabled',true);
    	var vIds = $(this).val();
    	var userInfo = $(this).parent().parent().parent().find("td").eq(1)
	    var username = userInfo.text()
	    var uid = userInfo.find("span").attr("title")
	    $.confirm({
	        icon: 'fa fa-edit',
	        type: 'blue',
	        title: '修改<code>'+username+'</code>配置',
	        content: '<form  data-parsley-validate class="form-horizontal form-label-left">' +
			            '<div class="form-group">' +
			              '<label class="control-label col-md-3 col-sm-3 col-xs-12" for="last-name">角色分配<span class="required">*</span>' +
			              '</label>' +
			              '<div class="col-md-6 col-sm-6 col-xs-12">' +
                              '<select  required="required" class="form-control"  data-size="10" data-selected-text-format="count > 5" data-live-search="true" data-width="100%"   autocomplete="off"  class="form-control" name="modf_role"    required>' +
                                   	'<option name="modf_role" value="deploy">开发人员</option>' +
									'<option name="modf_role" value="manage">管理人员</option>' +
                              '</select>' +
			              '</div>' +                                           			
			          '</form>',
	        buttons: {
	            '取消': function() {},
	            '修改': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var role = this.$content.find("[name='modf_role'] option:selected").val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/apps/roles/" + vIds + '/',  
				            data:{
				            	"role":role,
				            	"project":get_url_param('id'),
				            	"user":uid
				            	},
				            error: function(request) {  
				            	new PNotify({
				                    title: 'Ops Failed!',
				                    text: request.responseText,
				                    type: 'error',
				                    styling: 'bootstrap3'
				                });       
				            },  
				            success: function(data) {  
				            	new PNotify({
				                    title: 'Success!',
				                    text: '配置修改成功',
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
				            	RefreshDeployRolesTable("#deployRolesList","/apps/config/?type=info&id="+get_url_param('id'))
				            }  
				    	});
	                }
	            }
	        }
	    });    
		$(this).attr('disabled',false);
	});
	
})