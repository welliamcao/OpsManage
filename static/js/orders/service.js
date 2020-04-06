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

var orderAuditStatusHtml = {
	    "1":'<span class="label label-danger">已拒绝</span>',
	    "2":'<span class="label label-info">审核中</span>',
	    "3":'<span class="label label-success">已授权</span> '
	}

var orderExecuteStatusHtml = {
		"0":'<span class="label label-warning">已提交</span>',
	    "1":'<span class="label label-info">处理中</span>',
	    "2":'<span class="label label-success">已完成</span>',
	    "3":'<span class="label label-warning">已回滚</span> ',
	    "4":'<span class="label label-default">已关闭</span> ',
	    "5":'<span class="label label-danger">执行失败</span> ',
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

function makeOrderLogsTableList(url){
	if ($('#ordersLogs').hasClass('dataTable')) {
		dttable = $('#ordersLogs').dataTable();
		dttable.fnClearTable(); //清空table
		dttable.fnDestroy(); //还原初始化datatable
	}	
	var data = requests('get',url)
    var columns = [		                   
                    {"data": "order"},
                    {"data": "operator"},
                    {"data": "operation_info"},
                    {"data": "audit_status"},
                    {"data": "execute_status"},
	                {"data": "operation_time"}			                			                
	               ]
    var columnDefs = [			                      
						{
							targets: [3],
							render: function(data, type, row, meta) {
						        return orderAuditStatusHtml[row.audit_status]
							},
						},
						{
							targets: [4],
							render: function(data, type, row, meta) {
						        return orderExecuteStatusHtml[row.execute_status]
							},
						}						
	    		      ]
    var buttons = [
			    					    
    ] 		    
    $('#ordersLogs').dataTable({
	    "dom": "Bfrtip",
	    "buttons":buttons,
		"bScrollCollapse": false, 				
	    "bRetrieve": true,			
		"destroy": true, 
		"data":	data,
		"columns": columns,
		"columnDefs" :columnDefs,			  
		"language" : language,
		"order": [[ 0, "desc" ]],
		"autoWidth": false	    			
	});    
}

function DynamicSelect(ids,value){
	$("#" + ids +" option").each(function(){ 
		$(this).prop("selected",false);   
	})
	$("#" + ids +" option[value='" + value +"']").prop("selected",true);	
	$("#" + ids).attr("disabled","")
	$('#'+ids).selectpicker('refresh');	
}

function makeUserSelect(ids,dataList){
	var binlogHtml = '<select required="required" class="selectpicker form-control" data-live-search="true"  data-size="10" data-width="100%" name="'+ ids +'" id="'+ids+'"  autocomplete="off"><option selected="selected" value="">选择一个用户</option>'
	var selectHtml = '';
	for (var i=0; i <dataList.length; i++){
		selectHtml += '<option value="'+ dataList[i]["id"] +'">'+ dataList[i]["username"] +'</option>' 					 
	};                        
	binlogHtml =  binlogHtml + selectHtml + '</select>';
	$('#'+ids).html(binlogHtml)		
	$('#'+ids).selectpicker('refresh');		
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
		if ((data["order_audit_status"] ==3 && data["order_execute_status"] == 1) || (data["order_audit_status"] ==3 && data["order_execute_status"] == 0)){
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
			},
	    	error:function(response){
	    		btnObj.removeAttr('disabled');
	        	new PNotify({
	                title: 'Warning!',
	                text: '工单更新失败',
	                type: 'warning',
	                styling: 'bootstrap3'
	            }); 
	    	}
		});	
	}) 
})
