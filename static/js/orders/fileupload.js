function makeFileUploadResultTable(dataList){
	var trHtml = '';
	for (var i = 0; i < dataList.length; ++i) {
		if (dataList[i]["status"] == "success" ){
			var stauts = '<span class="label label-success">成功</span>'
		}else{
			var stauts = '<span class="label label-danger">失败</span>'
		}		
		trHtml += '<tr>'+ 
						'<td>'+ dataList[i]["fname"] +'</td>'+ 
						'<td>'+ dataList[i]["host"] +'</td>'+ 
						'<td>'+ dataList[i]["dest"] + '</td>'+ 
						'<td>'+ dataList[i]["size"] + '</td>'+ 
						'<td>'+ dataList[i]["changed"] + '</td>'+ 
						'<td  class="text-center">'+ stauts + '</td>'+ 
						'<td>'+ dataList[i]["msg"] + '</td>'+
		          '</tr>'
	};	
	var vTableHtml = '<div id="result">' +
						'<table class="table table-bordered" id="result-table">' + 
							'<caption>文件分发结果</caption>' + 
							'<thead>' + 
								'<tr>'+
									'<th>文件名</th>'+
									'<th>目标主机</th>'+ 									
									'<th>目标路径</th>'+
									'<th>文件大小(MB)</th>'+
									'<th>是否变更</th>'+
									'<th class="text-center">分发结果</th>'+
									'<th>失败原因</th>'+
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

$(document).ready(function() {
	
	makeOrderLogsTableList("/api/orders/logs/"+ get_url_param("id") +"/")
	
	$(function() {
		var data = requests('get','/api/orders/'+get_url_param("id")+'/')
		$("#order_time").val(data["start_time"]+' - '+ data["end_time"]).attr("disabled","")
		$("#order_audit_status").html(orderAuditStatusHtml[data["order_audit_status"]])
		$("#fileupload_order_subject").val(data["order_subject"]).attr("disabled","")
		$("#order_content").val(data["detail"]["order_content"]).attr("disabled","")
		AssetsSelect("custom",requests('get','/api/assets/?assets_type=ser'),data["detail"]["dest_server"])
		AssetsSelect("files",data["detail"]["files"])
		$("#dest_path").val(data["detail"]["dest_path"]).attr("disabled","")
		$("#ans_uuid").val(uuid())
		switch(data["order_audit_status"])
		{
		case 3:
			$("#fileuploadbtn").val(get_url_param("id")).attr("disabled",false)
		  break;			  
		}
	})
	
    $("button[name='btn-fileupload-run']").on('click', function() {
    	var value = $(this).val();
    	var btnObj = $(this)
    	btnObj.attr('disabled',true);
		var serverList = []
		$("select[name='custom'] option:selected").each(function(){
			serverList.push($(this).val());
        });	
		var fileList = []
		$("select[name='files'] option:selected").each(function(){
			fileList.push($(this).val());
        });		
		if (value>=1 && serverList.length && fileList.length){
			$("#result").html('<i class="fa fa-spinner"> 服务器正在处理...</i>');
	    	$.ajax({  
	            cache: true,  
	            type: "POST",  
	            url:"/order/fileupload/handle/",  
	            data:{
	            	"id":value,
	            	"type":"exec_fileupload",
	            	"server":serverList,
	            	"files":fileList
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
/*						$("#order_audit_status").html(orderAuditStatusHtml[response["data"]["status"]])*/						
						makeFileUploadResultTable(response["data"])
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
					         	$("#order_audit_status").html(orderAuditStatusHtml[status])
					         	$("#fileuploadbtn").attr('disabled',true);	
					         	makeOrderLogsTableList("/api/orders/logs/"+ get_url_param("id") +"/")
				            }  
				    	});
	                }
	            }
	        }
	    });		
	}
	
	function confirmorderAuditStatusHtml(ids,status){
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
	         	$("#order_audit_status").html(orderAuditStatusHtml[status])
	         	$("#fileuploadbtn").attr('disabled',true);
	         }  
	 	});		
	}
})
