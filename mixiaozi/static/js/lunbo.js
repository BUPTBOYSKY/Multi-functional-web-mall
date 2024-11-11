window.onload=function(){
    //第一个幻灯 
    var pic_lis=document.getElementById('b_pic').getElementsByTagName('li');
    var an_lis=document.getElementById('b_an').getElementsByTagName('li');
    an_lis[0].style.background='#b31114';
    var c=0;

    function h_slide(){
        c++;
        if(c==pic_lis.length){c=0;}
        for(var i=0; i<pic_lis.length; i++){
            pic_lis[i].style.display='none';
            an_lis[i].style.background='#fff';
        }
        pic_lis[c].style.display='block';
        an_lis[c].style.background='#b31114';	
    }
    var timer=setInterval(h_slide,4000);

    for(var j=0; j<pic_lis.length; j++){
        an_lis[j].index=j;
        an_lis[j].onmouseover=function(){
            index=this.index;
            clearInterval(timer);
            for(var k=0; k<an_lis.length; k++){
                pic_lis[k].style.display='none';
                an_lis[k].style.background='#fff';
            }
            pic_lis[index].style.display='block';
            an_lis[index].style.background='#b31114';
        }

        an_lis[j].onmouseout=function(){
            timer=setInterval(h_slide,4000);
        }
    }
}