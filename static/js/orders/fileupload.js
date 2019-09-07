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
				var text = dataList[i]["detail"]["ip"]
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


$(document).ready(function() {
	
	$(function() {
		var data = requests('get','/order/info/?type='+get_url_param("type")+'&&id='+get_url_param("id"))
		$("#order_status").html(orderStatus[data["data"]["order_status"]])
		$("#fileupload_order_subject").val(data["data"]["order_subject"]).attr("disabled","")
		$("#order_content").val(data["data"]["detail"]["upload"]["order_content"]).attr("disabled","")
		AssetsSelect("custom",requests('get','/api/assets/?assets_type=ser'),data["data"]["detail"]["upload"]["dest_server"])
		AssetsSelect("files",data["data"]["detail"]["files"])
		$("#dest_path").val(data["data"]["detail"]["upload"]["dest_path"]).attr("disabled","")
		$("#ans_uuid").val(uuid())
		switch(data["data"]["order_status"])
		{
		case 8:
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
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 
	            },  
	            success: function(response) {  
	            	btnObj.attr('disabled',false);
					if (response["code"] == 200){
/*						$("#order_status").html(orderStatus[response["data"]["status"]])*/						
						makeFileUploadResultTable(response["data"])
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
					         	$("#fileuploadbtn").attr('disabled',true);				            	
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
	         	$("#fileuploadbtn").attr('disabled',true);
	         }  
	 	});		
	}
})