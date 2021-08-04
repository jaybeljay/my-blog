$(document).ready(function() {
	
	var csrf_token = $('#voting [name="csrfmiddlewaretoken"]').val();
	
	$('#voting [data-action="upvote"]').click(function() {
		
		var vote_type = $(this).data('type');
		var pk = $(this).data('id');
		var action = $(this).data('action');
		
		if ($(this).hasClass('upvote selected')) {
			$.ajax ({
				type: 'POST',
				url: "upvote/",
				data: {
					'csrfmiddlewaretoken': csrf_token,
					'obj': pk
				},
			success: function(json) {
				$(this).removeClass('');
				$(this).addClass('upvote text-muted');
				$('#rating').text(json.rating);
			}
		})
		} else {
			$.ajax ({
				type: 'POST',
				url: "upvote/",
				data: {
					'csrfmiddlewaretoken': csrf_token,
					'obj': pk
			},
			success: function(json) {
				if ($('#voting [data-action="downvote"]').hasClass('downvote selected')) {
					$('#voting [data-action="downvote"]').removeClass('downvote selected');
					$('#voting [data-action="downvote"]').addClass('downvote text-muted');
				} else {
					$(this).removeClass('upvote text-muted');
					$(this).addClass('upvote selected');
					$('#rating').text(json.rating);
				}
			}
		})
	}

	return false;

})


	$('#voting [data-action="downvote"]').click(function() {

		var vote_type = $(this).data('type');
		var pk = $(this).data('id');
		var action = $(this).data('action');
		
		if ($(this).hasClass('downvote selected')) {
			$.ajax ({
			type: 'POST',
			url: 'downvote/',
			data: {
				'csrfmiddlewaretoken': csrf_token,
				'obj': pk
			},
			success: function(json) {
				$(this).removeClass('downvote selected');
				$(this).addClass('downvote text-muted');
				$('#rating').text(json.rating);
			}
		})
		} else {
			$.ajax ({
			type: 'POST',
			url: 'downvote/',
			data: {
				'csrfmiddlewaretoken': csrf_token,
				'obj': pk
			},
			success: function(json) {
				if ($('#voting [data-action="upvote"]').hasClass('upvote selected')) {
					$('#voting [data-action="upvote"]').removeClass('upvote selected');
					$('#voting [data-action="upvote"]').addClass('upvote text-muted');
				} else {
					$(this).removeClass('downvote text-muted');
					$(this).addClass('downvote selected');
					$('#rating').text(json.rating);
				}
			}
		})
	}
	
	return false;
	
})
	
	let rating_divs = document.querySelectorAll('.rating');
	
	let change_color = function(elem, nmb) {
		
		if (nmb > 0) {
			return $(elem).html('<span style="color: green">' + nmb + '</span>');
		} else if (nmb < 0) {
			return $(elem).html('<span style="color: red">' + nmb + '</span>');
		}
	}
	
	for (let elem of rating_divs) {
		let int_nmb = parseInt(elem.textContent);
		change_color(elem, int_nmb);
	}
	
	let rating_div = document.getElementById('rating');
	if (rating_div) {
		let rating_div_int = parseInt(rating_div.textContent);
		change_color(rating_div, rating_div_int);
		
		let observer = new MutationObserver(mutations => {
		for (let mutation of mutations) {
			for (let node of mutation.addedNodes) {
				if (node instanceof Text) {
					let int_rating = parseInt(node.textContent);	
					console.log(int_rating);
					change_color(rating_div, int_rating);
					}
				}
			}
		})

		config = {
			childList: true,
			characterData: true,
		}
		
		observer.observe(rating_div, config);
	}


	$('#create_comment input').click(function(e) {
			
			e.preventDefault();
			var form_comment = document.forms.create_comment;
			var formData = new FormData(form_comment);
			var comment_text = formData.get('comment_text');
			
			$.ajax({
				type: 'POST',
				url: 'comment/',
				data: {
					csrfmiddlewaretoken: csrf_token,
					comment_text: comment_text,
				},
				success: function(response) {
					$('.commentslist').replaceWith(response);
				}
			});
		})
})