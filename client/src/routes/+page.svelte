<script lang="ts">
	import Button from '$lib/components/button.svelte';

	let INN: string = '6208005457';
	let UKEP: string = 'test';
	let MCHD: string = 'test';
	let email: string = 'test@mail.ru';

	$: message = '';

	const handleSubmit = async () => {
		message = '';
		const response = await fetch('http://0.0.0.0:8000/api/input/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ INN, UKEP, MCHD, email })
		});

		const result = (await response.json().catch((cause: unknown) => {
			console.error(new Error('Result json parse failed', { cause }));
		})) as Record<string, string>;

		message = result.message;
	};
</script>

<form action="POST" on:submit|preventDefault={handleSubmit}>
	<label for="INN">
		ИНН
		<input type="number" name="INN" id="INN" bind:value={INN} />
	</label>
	<label for="UKEP">
		УКЭП
		<textarea name="UKEP" id="UKEP" bind:value={UKEP} />
	</label>
	<label for="MCHD">
		МЧД
		<textarea name="MCHD" id="MCHD" bind:value={MCHD} />
	</label>
	<label for="email">
		Электронная почта
		<input type="email" name="email" id="email" bind:value={email} />
	</label>
	<Button />

	<p>
		{message}
	</p>
</form>

<style>
	form {
		max-width: 400px;
		display: flex;
		flex-direction: column;
		row-gap: 12px;
		padding: 12px;
	}

	label {
		display: flex;
		flex-direction: column;
		row-gap: 4px;
	}

	input,
	textarea {
		all: unset;
		padding: 8px 12px;
		border-radius: 4px;
		border: 1px solid var(--color-text-accent);
	}

	input[type='number'] {
		-moz-appearance: textfield;
	}
	input::-webkit-outer-spin-button,
	input::-webkit-inner-spin-button {
		-webkit-appearance: none;
	}

	textarea {
		resize: vertical;
	}
</style>
