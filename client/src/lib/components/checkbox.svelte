<script lang="ts">
	type CheckboxType = 'director' | 'agreement';

	export let id: CheckboxType;
	export let isChecked = false;
	export let name: CheckboxType;
</script>

<label for={id}>
	<input bind:checked={isChecked} type="checkbox" {name} {id} />
	<slot />
</label>

<style>
	label {
		display: block;
	}
</style>
