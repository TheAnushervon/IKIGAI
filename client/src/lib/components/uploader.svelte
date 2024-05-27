<script lang="ts">
	import type { ChangeEventHandler, DragEventHandler } from 'svelte/elements';

	// export let files: FileList;

	let files: File[] = [];
	let dropText = 'Перетащите файлы сюда';

	const handleDrop: DragEventHandler<HTMLButtonElement> = ({ dataTransfer }) => {
		if (!dataTransfer) return;
		const newFiles = Array.from(dataTransfer.files);
		files = [...files, ...newFiles];
	};

	const handleFileChange: ChangeEventHandler<HTMLInputElement> = ({ currentTarget }) => {
		if (!currentTarget.files) return;
		const newFiles = Array.from(currentTarget.files);
		files = [...files, ...newFiles];
	};

	$: {
		console.log(files);
	}
</script>

<button
	class="drop-zone"
	aria-label={dropText}
	on:drop|preventDefault={handleDrop}
	on:dragover|preventDefault
	on:dragleave|preventDefault
>
	{#if files.length}
		<ul>
			{#each files as file}
				<li class="file">{file.name}</li>
			{/each}
		</ul>
	{/if}
	<p>{dropText}</p>
</button>
<input type="file" id="fileInput" multiple on:change={handleFileChange} />
<label for="fileInput" class="upload-button">Выберите файлы</label>

<style>
	.drop-zone {
		border: 2px dashed #ccc;
		padding: 20px;
		text-align: center;
	}

	input[type='file'] {
		display: none;
	}

	.upload-button {
		display: inline-block;
		margin-top: 1rem;
		padding: 0.5rem 1rem;
		background-color: #0073e6;
		color: white;
		cursor: pointer;
		border: none;
		border-radius: 4px;
	}
</style>
