const ui = () => {
	return /*html*/ `
		<div>
			<h1 id="top_title">Hello my first ui</h1>
		</div>
	`;
}

function init() {
	document.body.innerHTML = ui();
}
