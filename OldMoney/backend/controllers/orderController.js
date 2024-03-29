import asyncHandler from 'express-async-handler';
import Order from '../models/orderModel.js';


const createOrder = asyncHandler(async (req, res) => {
	const {
		orderItems,
		shippingAddress,
		paymentMethod,
		itemsPrice,
		taxPrice,
		shippingPrice,
		totalPrice,
	} = req.body;

	if (orderItems && orderItems.length === 0) {
		res.status(400);
		throw new Error('No order item');
	} else {
		const order = new Order({
			orderItems,
			user: req.user._id,
			shippingAddress,
			shippingPrice,
			itemsPrice,
			taxPrice,
			paymentMethod,
			totalPrice,
		});

		const createdOrder = await order.save();
		res.status(201).json(createdOrder);
	}
});



    // populate helps us avoid 2 separate requests. Here, given that user was initially just an id 
    // when we made a req to /api/orders/order_id, we had it use populate() to fetch other info about this user
    // namely 'name' and 'email'.



const getOrderById = asyncHandler(async (req, res) => {
	const order = await Order.findById(req.params.id).populate(
		'user',
		'name email'
	);

	if (order) {
		res.json(order);
	} else {
		res.status(404);
		throw new Error('Order not found');
	}
});
const updateOrderToPaid = asyncHandler(async (req, res) => {
	const order = await Order.findById(req.params.id);

	if (order) {
		order.isPaid = true;
		order.paidAt = Date.now();
		order.paymentResult = {
			id: req.body.id,
			state: req.body.state,
			update_time: req.body.update_time,
			email_address: req.body.email_address,
		};

		const updatedOrder = await order.save();
		res.json(updatedOrder);
	} else {
		res.status(404);
		throw new Error('Order not found');
	}
});





const getMyOrders = asyncHandler(async (req, res) => {
	console.log("reached here!")
	const orders = await Order.find({ user: req.user._id });
	res.json(orders);
});

export { createOrder, getMyOrders, getOrderById, updateOrderToPaid };
