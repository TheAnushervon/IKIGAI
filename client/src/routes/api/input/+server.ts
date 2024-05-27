import { error, json, type RequestHandler } from '@sveltejs/kit';

interface UserRequestBody {
	INN: string;
	UKEP: string;
	MCHD: string;
	email: string;
}

const BACKEND_URL = process.env.BACKEND_URL || 'http://server:8000';

export const POST: RequestHandler = async ({ locals, request }) => {
	const { logger } = locals;
	const body = (await request.json()) as UserRequestBody;

	if (!body) {
		logger.error('No body in request');
		throw error(400);
	}

	const { INN, UKEP, MCHD, email } = body;

	if (!INN) {
		logger.error('No INN in request');
		throw error(400);
	}
	if (!UKEP) {
		logger.error('No UKEP in request');
		throw error(400);
	}
	if (!MCHD) {
		logger.error('No MCHD in request');
		throw error(400);
	}
	if (!email) {
		logger.error('No email in request');
		throw error(400);
	}

	const response = await fetch(`${BACKEND_URL}/api/input/`);

	if (!response.ok) {
		logger.error('Response is not OK');
		throw error(response.status, response.statusText);
	}

	const result = await response.json();

	return json({ isSuccess: true, result });
};
