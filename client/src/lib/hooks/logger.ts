import type { Handle } from '@sveltejs/kit';
import pino from 'pino';

const pinoLogger = pino({
	level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
	...(process.env.NODE_ENV !== 'production' && {
		transport: {
			target: 'pino-pretty',
			options: {
				colorize: true
			}
		}
	})
});

export const logger: Handle = async ({ event, resolve }) => {
	event.locals.logger = pinoLogger;
	const response = await resolve(event);
	const { method, url } = event.request;
	event.locals.logger.info(`${method} ${url} ${response.status}`);
	return response;
};
