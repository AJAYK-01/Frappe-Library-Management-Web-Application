<script>
	export let parent;
	export let submitForm;

	import { getModalStore } from '@skeletonlabs/skeleton';
	import { modalAlert } from '../../functions/showAlert';
	const modalStore = getModalStore();

	let name = $modalStore[0].member_name ?? '';
	let debt = $modalStore[0].member_debt ?? 0.0;
	let disableSubmit = false;

	function validateDebt() {
		if (debt < 0.0) {
			debt = 0;
		}
	}

	async function onFormSubmit() {
		if (debt < 0.0) {
			modalAlert(modalStore, 'Debt must not be negative');
		}
		disableSubmit = true;

		// edit member details
		if ($modalStore[0].member_id) {
			try {
				const res = await submitForm($modalStore[0].member_id, name, debt);
				if (res.ok) {
					modalAlert(modalStore, `Member ${$modalStore[0].member_id} succesfully edited`);
					setTimeout(() => window.location.reload(), 3000);
				} else {
					modalAlert(modalStore, 'Member edit failed: ' + res.status);
				}
			} catch (error) {
				modalAlert(modalStore, 'Member edit failed: ' + error.message);
			}
		}
		// add new member
		else {
			try {
				const res = await submitForm(name, debt);
				const json = await res.json();
				const member_id = json.id;
				modalAlert(modalStore, `Member succesfully created with id ${member_id}`);
				setTimeout(() => window.location.reload(), 3000);
			} catch (error) {
				modalAlert(modalStore, 'Member creation failed: ' + error.message);
			}
		}
		modalStore.close();
	}
</script>

{#if $modalStore[0]}
	<div class="modal-example-form rounded-lg card px-6 pt-4 pb-8 w-modal shadow-xl space-y-4">
		<header class="text-2xl my-2">{$modalStore[0].title ?? 'Add New Member'}</header>

		<form on:submit={onFormSubmit} class="modal-form">
			<label class="member_name_add">
				<span>Name</span>
				<input
					class="input rounded-full py-1 px-3 mt-1 mb-5"
					type="text"
					bind:value={name}
					placeholder="Enter member name..."
					required
				/>
			</label>
			<label class="member_name_add">
				<span>Outstanding Debt</span>
				<div class="mt-1 input-group rounded-full input-group-divider grid-cols-[auto_1fr_auto]">
					<div class="input-group-shim"><i class="fas fa-rupee-sign" /></div>
					<input
						class="py-1 px-3"
						type="number"
						step="0.01"
						bind:value={debt}
						on:input={validateDebt}
						placeholder="Enter outstanding debt if any..."
						required
					/>
				</div>
			</label>

			<footer class="modal-footer mt-5 {parent.regionFooter}">
				<button class="btn rounded-full {parent.buttonNeutral}" on:click={parent.onClose}
					>{parent.buttonTextCancel}</button
				>
				<button
					disabled={disableSubmit}
					type="submit"
					class="btn variant-filled-secondary rounded-full {parent.buttonPositive}">Submit</button
				>
			</footer>
		</form>
	</div>
{/if}
