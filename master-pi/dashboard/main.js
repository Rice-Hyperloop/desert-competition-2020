let data = {};

async function update() {
	let response = await fetch('data.json');
	data = await response.json();
	updateData(data);
}

async function sendCommand(command) {
	await fetch('send_command', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(command)
	});
}

function updateData(data) {
	for (let [name, value] of Object.entries(data)) {
		let element = document.getElementById(name);
		if (element) {
			element.value = value;
		}
	}
}

window.setInterval(update, 250);
