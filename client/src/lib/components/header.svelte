<script lang="ts">
	import Logo from '$lib/assets/icons/logo.svg';
</script>

<header>
	<img src={Logo} alt="logo" class="logo" />
</header>

<style>
	.logo {
		padding: 12px;
		max-width: 400px;
	}

	header {
		height: 92px;
		position: sticky;
		top: 0;
		z-index: var(--ifm-z-index-fixed);
	}
</style>
