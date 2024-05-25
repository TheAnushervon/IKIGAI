import { logger } from '$lib/hooks/logger';
import type { Handle, HandleServerError } from '@sveltejs/kit';

import { sequence } from '@sveltejs/kit/hooks';

export const handle: Handle = sequence(logger, async ({ event, resolve }) => {
	return await resolve(event);
});

export const handleError: HandleServerError = ({ event, error }) => {
	event.locals.logger.error(error);

	if (!(error instanceof Error)) return;

	return {
		message: error.message
	};
};
