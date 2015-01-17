


var postComment = function() {
	for(i = 0 ; i < interests.length; i++){		
		if ($(".interests").html()=="") {
			$(".interests").append("Interests : " + interests[i]);
		} else {
			$(".interests").append("<br>	" + interests[i]);
		}
		
	}
};

$(document).ready(function () {
		// adding a wall post
	    $(".newCommentPost").submit(function (e) {
	    	
	        if ($(".commentText").val() == "") {
	            alert("You didn't write a comment, try again!");
	        } else {
	        	alert($(".commentText").val());
	            // var postData = $(this).serializeArray();
	            // var formURL = $(this).attr("action");
	            // $.ajax({
	            //     url: formURL,
	            //     type: "POST",
	            //     data: postData,
	            //     success: function (data, textStatus, jqXHR) {
	            //         // clearing fields
	            //     	wallposts = [];
	            //         $(".wallpost").val("");
	            //         setTimeout(function() {getWallposts();}, 500);
	            //         //alert("Wallpost was sucessfully added!");
	            //     },
	            //     error: function (jqXHR, textStatus, errorThrown) {
	            //         alert("Wallpost was not posted, please try again. " + errorThrown);
	            //     }
	            // });
	        }
	        e.preventDefault();
	    });	

});