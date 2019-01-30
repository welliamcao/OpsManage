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


$(document).ready(function() {
	
	$(function() {
		var data = requests('get','/order/info/?type='+get_url_param("type")+'&&id='+get_url_param("id"))
		$("#order_status").html(orderStatus[data["data"]["order_status"]])
		$("#fileupload_order_subject").val(data["data"]["order_subject"]).attr("disabled","")
		$("#order_content").val(data["data"]["detail"]["upload"]["order_content"]).attr("disabled","")
		AssetsSelect("custom",requests('get','/api/assets/'),data["data"]["detail"]["upload"]["dest_server"])
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
			$("#result").html("服务器正在处理，请稍等。。。");
			/* 轮训获取结果 开始  */
		   var interval = setInterval(function(){  
		        $.ajax({  
		            url : '/deploy/run/',  
		            type : 'post', 
		            data:$('#run_fileupload_order').serialize(),
		            success : function(result){
		            	if (result["msg"] !== null ){
		            		$("#result").append("<p>"+result["msg"]+"</p>"); 
		            		document.getElementById("scrollToTop").scrollIntoView(); 
		            		if (result["msg"].indexOf("[Done]") == 0){
		            			clearInterval(interval);
		            			$.confirm({
		            			    title: '执行确认',
		            			    content: "确认工单状态",
		            			    type: 'red',
		            			    buttons: {
		            			    	完成: {
		            			            text: '完成',
		            			            btnClass: 'btn-blue',
		            			            action: function(){
		            			            	confirmOrderStatus(value,5)	
		            			            }
		            			        },
		            			    	失败: {
		            			            text: '失败',
		            			            btnClass: 'btn-red',
		            			            action: function(){			
		            			            	setOrderFailed(value,9)	
		            			            }
		            			        },		            			        
		            			        继续: function () {
		            			        	btnObj.removeAttr('disabled');
		            			        	return true;
		            			        }
		            			    }		            			    
		            			});			     
		            		}
		            	}
		            },
			    	error:function(response){
			    		btnObj.removeAttr('disabled');
			    		clearInterval(interval);
			    	}	            
		        });  
		    },1000); 			
			
	    	$.ajax({  
	            cache: true,  
	            type: "POST",  
	            url:"/order/fileupload/handle/",  
	            data:{
	            	"id":value,
	            	"type":"exec_fileupload",
	            	"server":serverList,
	            	"files":fileList,
	            	"ans_uuid":$("#ans_uuid").val()
	            	},
	            error: function(response) {
	            	btnObj.attr('disabled',false);
	            	new PNotify({
	                    title: 'Ops Failed!',
	                    text: response.responseText,
	                    type: 'error',
	                    styling: 'bootstrap3'
	                }); 
	            	clearInterval(interval);
	            },  
	            success: function(response) {  
	            	btnObj.attr('disabled',false);
					if (response["code"] == 200){
/*						$("#order_status").html(orderStatus[response["data"]["status"]])*/
						
					}
					else {
			    		$.alert({
			    		    title: '文件分发失败',
			    		    content: response["msg"],
			    		    type: 'red',
			    		});	
			    		clearInterval(interval);
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