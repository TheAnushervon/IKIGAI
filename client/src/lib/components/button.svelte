<button type="submit">Отправить</button>

<style>
	button {
		all: unset;
		color: var(--color-text-accent);
		padding: 8px 12px;
		border: 1px solid var(--color-text-accent);
		border-radius: 8px;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	button:hover {
		background-color: rgba(var(--color-text-accent-rgb), 0.1);
	}

	button:focus-visible {
		outline: 2px solid var(--color-text-accent);
	}
</style>
