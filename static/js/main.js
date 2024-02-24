(function() {
	"use strict";

	// Easy selector helper function
	const select = (el, all = false) => {
		el = el.trim()
		if (all) {
			return [...document.querySelectorAll(el)]
		} else {
			return document.querySelector(el)
		}
	}

	// Easy event listener function
	const on = (type, el, listener, all = false) => {
		if (all) {
			select(el, all).forEach(e => e.addEventListener(type, listener))
		} else {
			select(el, all).addEventListener(type, listener)
		}
	}

	// Easy on scroll event listener 
	const onscroll = (el, listener) => {
		el.addEventListener('scroll', listener)
	}

	// side menu toggle
	if (select('.toggle-sidebar-btn')) {
		on('click', '.toggle-sidebar-btn', function(e) {
			select('#sidebar').classList.toggle('expand')
		})

		select('body').classList.add('toggle-sidebar');
	}

	// Function to hide modal backdrop
	function hideModalBackdrop() {
		// Find the modal backdrop element
		var modalBackdrop = document.querySelector('.modal-backdrop');
		// If modal backdrop exists, hide it
		if (modalBackdrop) {
			modalBackdrop.style.display = 'none';
		}
	}

	// Detect page redirection (e.g., after clicking a link)
	document.querySelector('#wrapper').addEventListener('click', function(event) {
		// Hide modal backdrop after redirection
		hideModalBackdrop();
	});

})();