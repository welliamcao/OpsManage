//fork from https://guguji5.github.io/bs-modal-dragable/bs-modal-dragable.html
var dragModal={
    mouseStartPoint:{"left":0,"top":  0},
    mouseEndPoint : {"left":0,"top":  0},
    mouseDragDown : false,
    basePoint : {"left":0,"top":  0},
    moveTarget:null,
    topleng:0
}

$(document).on("mousedown",".modal-header",function(e){
    //webkit内核和火狐禁止文字被选中
    $('body').addClass('modal-select')
    //ie浏览器禁止文字选中
    document.body.onselectstart=document.body.ondrag=function(){
        return false;
        }
    if($(e.target).hasClass("close"))//点关闭按钮不能移动对话框  
        return;  
    dragModal.mouseDragDown = true;  
    dragModal.moveTarget = $(this).parent().parent();         
    dragModal.mouseStartPoint = {"left":e.clientX,"top":  e.pageY};  
    dragModal.basePoint = dragModal.moveTarget.offset();  
    dragModal.topLeng=e.pageY-e.clientY;
});  
$(document).on("mouseup",function(e){       
    dragModal.mouseDragDown = false;  
    dragModal.moveTarget = undefined;  
    dragModal.mouseStartPoint = {"left":0,"top":  0};  
    dragModal.basePoint = {"left":0,"top":  0};  
});  
$(document).on("mousemove",function(e){  
    if(!dragModal.mouseDragDown || dragModal.moveTarget == undefined)return;          
    var mousX = e.clientX;  
    var mousY = e.pageY;  
    if(mousX < 0)mousX = 0;  
    if(mousY < 0)mousY = 25;  
    dragModal.mouseEndPoint = {"left":mousX,"top": mousY};  
    var width = dragModal.moveTarget.width();  
    var height = dragModal.moveTarget.height();
    var clientWidth=document.body.clientWidth
    var clientHeight=document.body.clientHeight;
    if(dragModal.mouseEndPoint.left<dragModal.mouseStartPoint.left - dragModal.basePoint.left){
        dragModal.mouseEndPoint.left=0;
    }
    else if(dragModal.mouseEndPoint.left>=clientWidth-width+dragModal.mouseStartPoint.left - dragModal.basePoint.left){
        dragModal.mouseEndPoint.left=clientWidth-width-38;
    }else{
        dragModal.mouseEndPoint.left =dragModal.mouseEndPoint.left-(dragModal.mouseStartPoint.left - dragModal.basePoint.left);//移动修正，更平滑  
        
    }
    if(dragModal.mouseEndPoint.top-(dragModal.mouseStartPoint.top - dragModal.basePoint.top)<dragModal.topLeng){
        dragModal.mouseEndPoint.top=dragModal.topLeng;
    }else if(dragModal.mouseEndPoint.top-dragModal.topLeng>clientHeight-height+dragModal.mouseStartPoint.top - dragModal.basePoint.top){
        dragModal.mouseEndPoint.top=clientHeight-height-38+dragModal.topLeng;
    }
    else{
        dragModal.mouseEndPoint.top = dragModal.mouseEndPoint.top - (dragModal.mouseStartPoint.top - dragModal.basePoint.top);           
    }
    dragModal.moveTarget.offset(dragModal.mouseEndPoint);  
});   
$(document).on('hidden.bs.modal','.modal',function(e){
    $('.modal-dialog').css({'top': '0px','left': '0px'})
    $('body').removeClass('select')
    document.body.onselectstart=document.body.ondrag=null;
}) 