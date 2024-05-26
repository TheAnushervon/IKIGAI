<script lang="ts">
	import 'normalize.css';
	import '../app.css';
	import Header from '$lib/components/header.svelte';
</script>

<svelte:head>
	<link rel="icon" type="image/png" href="/favicon.png" />
</svelte:head>

<Header />
<slot />

<style>
	:root {
		--color-text-primary: #e3e3e3;
		--color-text-accent: #00ffd8;
		--color-text-accent-rgb: 0, 255, 216;
		--color-background-primary: #1b1b1d;
		--color-background-secondary: #242526;
		--color-border-primary: #444950;
	}
</style>
