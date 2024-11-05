function bindEmailCaptchaClick() {
    // ‘#’ 用于id获取元素
    $("#captcha-btn").click(function (event) {
        // $this: 代表的是当前按钮的jquery对象
        var $this = $(this);

        // 阻止默认的提交表单事件
        event.preventDefault();
        // 通过name获取元素
        var email = $("input[name='email']").val();
        $.ajax({
            url: "/auth/captcha/email?email="+email,
            method: "GET",
            success:function (result) {
                var code = result['code'];
                if (code == 200){
                    var countdown = 5;
                    // 开始倒计时之前，先将按钮的点击事件取消
                    $this.off('click');
                    var timer = setInterval(function (){
                        $this.text(countdown);
                        countdown -= 1;
                        // 倒计时结束的时候执行
                        if (countdown <= 0) {
                            // 清掉定时器
                            clearInterval(timer);
                            // 将按钮的文本设置为原来的
                            $this.text('获取验证码');
                            // 重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                    alert('验证码发送成功，请注意查收！');
                }else {
                    alert(result['message']);
                }
            },
            fail: function (error) {
                console.log(error);
            }

        })

    });
}



// 在所有网页加载完成后才会执行, '$' 是jquery的简写
$(function () {
    bindEmailCaptchaClick();
});