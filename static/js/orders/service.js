function makeserviceResultTable(dataList){
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
		$("#order_status").html(orderAuditStatusHtml[data["order_status"]])
		$("#service_order_subject").val(data["order_subject"]).attr("disabled","")
		$("#service_order_content").val(data["detail"]["order_content"])
		makeUserSelect('service_order_executor',requests('get','/api/account/user/superior/',false))
		DynamicSelect('service_order_executor',data["order_executor"])	
		if ((data["order_audit_status"] ==2 && data["order_execute_status"] == 1) || (data["order_audit_status"] ==2 && data["order_execute_status"] == 0)){
			$("#servicebtn").val(get_url_param("id")).text("更新").attr({"disabled":false})
		}
	})
	
	$("button[name='btn-service-edit']").on('click', function() {	
		var btnObj = $(this);
		var required = ["order_content"];
	    var formData = new FormData();
	    formData.append('order_content',$('#service_order_content').val());    
		$.ajax({
/* 				dataType: "JSON", */
			url:'/api/orders/'+get_url_param("id")+'/', //请求地址
			type:"PUT",  //提交类似
		    processData: false,
		    contentType: false,				
			data:formData,  //提交参数
			success:function(response){
				btnObj.removeAttr('disabled');				
            	new PNotify({
                    title: 'Success!',
                    text: '工单修改成功',
                    type: 'success',
                    styling: 'bootstrap3'
                }); 
            	makeOrderLogsTableList("/api/orders/logs/"+ get_url_param("id") +"/")
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	        	new PNotify({
	                title: 'Warning!',
	                text: response.statusText,
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
	    	}
		});	
	}) 
})
