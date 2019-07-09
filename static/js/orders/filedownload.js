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

function get_url_param(name) {
	 var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
	 var r = window.location.search.substr(1).match(reg);
	 if (r != null) return unescape(r[2]); return null; 
}

function AssetsSelect(name,dataList,selectIds){
	if(!selectIds){selectIds=[]}
	switch(name)
	   {
		   case "project":
			   action = 'onchange="javascript:oBtProjectSelect(this);"'
		       break;			       
		   default:
			   action = ''	       
	   }
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" '+ action +' name="'+ name +'"autocomplete="off"><option value="">选择一个进行操作</option>'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		if(dataList[i][name+"_name"]){
			var text = dataList[i][name+"_name"]
			selectHtml += '<option value="'+ dataList[i]["id"] +'">'+text +'</option>'
		}else{
			switch(name)
			{
			case "custom":
				var text = dataList[i]["detail"]["ip"]+ ' | ' + dataList[i]["project"]+' | '+dataList[i]["service"]	
				var count = 0
				for (var j=0; j <selectIds.length; j++){
					if(selectIds[j]==dataList[i]["id"]){
						count = count + 1				
					}			
				}
				if (count > 0){
					selectHtml += '<option selected="selected" value="'+ dataList[i]["id"] +'">'+text +'</option>' 	
				}				
				break;
			case "files":
				var text =  dataList[i]["file_path"]
				selectHtml += '<option selected="selected" value="'+ dataList[i]["id"] +'">'+text +'</option>'
				break;
			default:
				var text = dataList[i]["name"]
				selectHtml += '<option value="'+ dataList[i]["id"] +'">'+text +'</option>'
				break;
			}				
		}					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	$("select[name='"+name+"']").html(binlogHtml)
	$("select[name='"+name+"']").selectpicker('refresh');		
}

var orderStatus = {
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
function requests(method,url,async){
	var ret = '';
	if(!async){async=false;} 
	$.ajax({
		async:async,
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

function makeFileDownloadResultTable(dataList){
	var trHtml = '';
	for (var i = 0; i < dataList.length; ++i) {
		if (dataList[i]["islnk"] ){
			var button = '<button type="button" class="btn btn-xs btn-default" disabled><abbr title="软连接不支持下载"><i class="fa  fa-cloud-download"></i></button>';
		}else if(dataList[i]["size"] > 500 ){
			var button = '<button type="button" class="btn btn-xs btn-default" disabled><abbr title="文件过大不支持下载"><i class="fa  fa-cloud-download"></i></button>';
		}else{
			var button = '<button type="button" name="download_button" class="btn btn-xs btn-default" onclick="downLoadOrderFiles(this,\'' + dataList[i]["path"] + '\',\'' + dataList[i]["host"] + '\',\'' + dataList[i]["aid"] +'\')"><abbr title="下载"><i class="fa  fa-cloud-download"></i></button>';
		}
		trHtml += '<tr><td>'+ i +'</td><td>'+ dataList[i]["host"] +'</td><td>'+ dataList[i]["path"] + '</td><td>' + dataList[i]["size"] + '</td><td>'+ dataList[i]["islnk"] + '</td><td class="text-center">'+ button +'</td></tr>'
	};	
	var vTableHtml = '<div id="result">' +
						'<table class="table table-bordered" id="result-table">' + 
							'<caption>选择文件进行下载</caption>' + 
							'<thead>' + 
								'<tr>'+
									'<th>id</th>'+
									'<th>主机</th>'+ 
									'<th>文件路径</th>'+
									'<th>文件大小(MB)</th>'+
									'<th>是否软连接</th>'+
									'<th>下载</th>'+
									'</tr>'+
							'</thead>'+
							'<tbody>' + trHtml +
							'</tbody>'+
						'</table>'+
					'</div>'
	$("#result").html(vTableHtml);
	$('#result-table').dataTable( {
	    "order": [[ 3, 'desc' ], [ 3, 'desc' ]],
	    "language" : language,
	});			
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

function downLoadOrderFiles(obj,path,host,id){
	$("button[name='download_button']").attr("disabled",true);
    var url = '/order/filedownload/handle/';	
    var data = {
			'id':get_url_param("id"),
			'path':path,
			'dest_host':host,
			'server[]':id,
			'type':'downloads'
     };
    downLoadFile({ //调用下载方法
	        	url:url,data:data
	        	}); 
    $("button[name='download_button']").attr("disabled",false);
}	

$(document).ready(function() {
	
	$(function() {
		var data = requests('get','/order/info/?type='+get_url_param("type")+'&&id='+get_url_param("id"))
		$("#order_status").html(orderStatus[data["data"]["order_status"]])
		$("#filedownload_order_subject").val(data["data"]["order_subject"]).attr("disabled","")
		$("#order_content").val(data["data"]["detail"]["download"]["order_content"]).attr("disabled","")
		AssetsSelect("custom",requests('get','/api/assets/?assets_type=ser'),data["data"]["detail"]["download"]["dest_server"])
		$("#dest_path").val(data["data"]["detail"]["download"]["dest_path"]).attr("disabled","")
		$("#ans_uuid").val(uuid())
		switch(data["data"]["order_status"])
		{
		case 8:
			$("#filedownloadbtn").val(get_url_param("id")).attr("disabled",false)
		  break;			  
		}
	})
	
    $("button[name='btn-filedownload-run']").on('click', function() {
    	var value = $(this).val();
    	var btnObj = $(this)
    	btnObj.attr('disabled',true);
		var serverList = []
		$("select[name='custom'] option:selected").each(function(){
			serverList.push($(this).val());
        });		
		if (value>=1 && serverList.length){	
			$("#result").html('<i class="fa fa-spinner"> 服务器正在处理...</i>');
	    	$.ajax({  
	            cache: true,  
	            type: "POST",  
	            url:"/order/filedownload/handle/",  
	            data:{
	            	"id":value,
	            	"type":"exec_filedownload",
	            	"server":serverList,
	            	},
	            error: function(response) {
	            	btnObj.attr('disabled',false);
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 
	            },  
	            success: function(response) {  
	            	btnObj.attr('disabled',false);
					if (response["code"] == 200){
						makeFileDownloadResultTable(response["data"])
					}
					else {
			    		$.alert({
			    		    title: '文件分发失败',
			    		    content: response["msg"],
			    		    type: 'red',
			    		});	
					};
	            }  
	    	});			
		}
		else{
    		$.alert({
    		    title: '文件分发失败',
    		    content: "请选择目标主机或者文件",
    		    type: 'red',
    		});	
    		btnObj.attr('disabled',false);
		}
    });		
	
	function setOrderFailed(ids,status){
	    $.confirm({
	        icon: 'fa fa-times',
	        type: 'blue',
	        title: '原因说明',
	        content: '<div class="form-group"><input type="text" value="" placeholder="请输入失败原因" class="param_name form-control" /></div>',
	        buttons: {
	            '取消': function() {},
	            '确认': {
	                btnClass: 'btn-blue',
	                action: function() {
	                    var cancel = this.$content.find('.param_name').val();
				    	$.ajax({  
				            cache: true,  
				            type: "PUT",  
				            url:"/api/orders/" + ids + '/', 
				            data:{
								"order_status":status,
								"order_cancel":cancel
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
				                    text: '工单状态修改成功',
				                    type: 'success',
				                    styling: 'bootstrap3'
				                }); 
					         	$("#order_status").html(orderStatus[status])
					         	$("#filedownloadbtn").attr('disabled',true);				            	
				            }  
				    	});
	                }
	            }
	        }
	    });		
	}
	
	function confirmOrderStatus(ids,status){
	   	 $.ajax({  
	         cache: true,  
	         type: "PUT",  
	         url:"/api/orders/" + ids + '/',  
	         data:{
				"order_status":status,
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
	                 text: '工单状态更改成功',
	                 type: 'success',
	                 styling: 'bootstrap3'
	             }); 
	         	$("#order_status").html(orderStatus[status])
	         	$("#filedownloadbtn").attr('disabled',true);
	         }  
	 	});		
	}
	
})