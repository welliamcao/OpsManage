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
	
	makeOrderLogsTableList("/api/orders/logs/"+ get_url_param("id") +"/")
	
	$(function() {
		var data = requests('get','/api/orders/'+get_url_param("id")+'/')
		$("#order_time").val(data["start_time"]+' - '+ data["end_time"]).attr("disabled","")
		$("#order_audit_status").html(orderAuditStatusHtml[data["order_audit_status"]])
		$("#filedownload_order_subject").val(data["order_subject"]).attr("disabled","")
		$("#order_content").val(data["detail"]["order_content"]).attr("disabled","")
		AssetsSelect("custom",requests('get','/api/assets/?assets_type=ser'),data["detail"]["dest_server"])
		$("#dest_path").val(data["detail"]["dest_path"]).attr("disabled","")
		$("#ans_uuid").val(uuid())
		switch(data["order_audit_status"])
		{
		case 3:
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
	                    text: response.statusText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 
	            },  
	            success: function(response) {  
	            	btnObj.attr('disabled',false);
					if (response["code"] == 200){
						makeFileDownloadResultTable(response["data"])
						makeOrderLogsTableList("/api/orders/logs/"+ get_url_param("id") +"/")
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
								"order_audit_status":status,
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
					         	$("#order_audit_status").html(orderStatus[status])
					         	$("#filedownloadbtn").attr('disabled',true);
					         	makeOrderLogsTableList("/api/orders/logs/"+ get_url_param("id") +"/")
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
				"order_audit_status":status,
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
	         	$("#order_audit_status").html(orderStatus[status])
	         	$("#filedownloadbtn").attr('disabled',true);
	         	makeOrderLogsTableList("/api/orders/logs/"+ get_url_param("id") +"/")
	         }  
	 	});		
	}
	
})
