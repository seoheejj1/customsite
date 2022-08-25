$(function () {
    // form confirm
    $(".manage_form").submit(function () {
        if (confirm("수정하시겠습니까?")) {
            return true;
        }
        return false;
    })

    // default
    $(".right_info").hide();
    $(".left_info_btn")
        .css("backgroundColor", "#212529")
        .css("color", "#fff");

    // site, account
    $(".right_info_btn").click(function () {
        $(".right_info_btn").css("backgroundColor", "#212529");
        $(".right_info_btn").css("color", "#fff");
        $(".right_info_btn")[0].disabled = true;
        $(".left_info_btn").css("backgroundColor", "#fff");
        $(".left_info_btn").css("color", "#212529");
        $(".left_info_btn")[0].disabled = false;
        $(".left_info").hide();
        $(".right_info").fadeIn();
    })
    $(".left_info_btn").click(function () {
        $(".left_info_btn").css("backgroundColor", "#212529");
        $(".left_info_btn").css("color", "#fff");
        $(".left_info_btn")[0].disabled = true;
        $(".right_info_btn").css("backgroundColor", "#fff");
        $(".right_info_btn").css("color", "#212529");
        $(".right_info_btn")[0].disabled = false;
        $(".right_info").hide();
        $(".left_info").fadeIn();
    })
    
    // point
    $("#tag_show").click(function () {
        $("#tag_hide")
            .css("backgroundColor", "#fff")
            .css("color", "#dc3545")
        $("#tag_hide")[0].disabled = false;
        $("#tag_show")
            .css("backgroundColor", "#0d6efd")
            .css("color", "#fff");
        $("#tag_show")[0].disabled = true;
        $("[name='tag_expose']").val("True");
    })
    $("#tag_hide").click(function () {
        $("#tag_hide")
            .css("backgroundColor", "#dc3545")
            .css("color", "#fff")
        $("#tag_hide")[0].disabled = true;
        $("#tag_show")
            .css("backgroundColor", "#fff")
            .css("color", "#0d6efd");
        $("#tag_show")[0].disabled = false;
        $("[name='tag_expose']").val("False");
    })

    // account
    $("#del_account").on('submit', function () {
        if (confirm("은행명: " + $(".bank").text() + "\n예금주: " + $(".depositer").text() + "\n계좌번호: " + $(".account").val() + "\n\n해당 계좌를 삭제하시겠습니까?")) {
            return true;
        }
        return false;
    })
    $("#account_add_btn").click(function () {
        if (confirm("계좌를 추가하시겠습니까?")) {
            $("#account_add").submit();
        }
    })
})