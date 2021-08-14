import { useEffect, useState } from 'react';
import axios from 'axios';
import { Link as RouterLink } from 'react-router-dom';
import { PayPalButton } from 'react-paypal-button-v2';
import {
  // Button,
  Flex,
  Heading,
  Box,
  Grid,
  Text,
  Image,
  Link,
} from '@chakra-ui/react';
import { useDispatch, useSelector } from 'react-redux';
import Message from '../components/Message';
import Loader from '../components/Loader';
import { getOrderDetails, payOrder } from '../actions/orderActions';
import { ORDER_PAY_RESET } from '../constants/orderConstants';

const OrderScreen = ({ match }) => {
  const orderId = match.params.id;
  const dispatch = useDispatch();

  const [sdkReady, setSdkReady] = useState(false);

  // Getting the orderDetails state from the Global store
  const orderDetails = useSelector((state) => state.orderDetails);
  const { order, loading, error } = orderDetails;

  //Paypal
  // get the orderPay state from the Global store
  // Destructure two values
  const orderPay = useSelector((state) => state.orderPay);
  const { loading: loadingPay, success: successPay } = orderPay;


  // Calculating Items' Price
  // !loading must be put or we will get an error.
  if (!loading) {
    order.itemsPrice = order.orderItems.reduce(
      (acc, currItem) => acc + currItem.price * (currItem.qty || 1),
      0
    );
  }

  useEffect(() => {
          //paypal script addition
    const addPayPalScript = async () => {
      // get the data from the backend. Remember that in our server.js, we had
      // written that if we get a req at /api/config/paypal then we must return the
      // paypal client id
      const { data: clientId } = await axios.get('/api/config/paypal');
        // building a script tag
      const script = document.createElement('script');
            // The following are requirements by paypal
      script.type = 'text/javascript';
      script.async = true;
          // attach script
      script.src = `https://www.paypal.com/sdk/js?client-id=${clientId}`;
         // once page loads
      script.onload = () => {
        setSdkReady(true);
      };
    // we know document.body will always be there for access, so
      // we use that
      document.body.appendChild(script);
    };




// if our order is false and sucessPay is done, then
    // we want to reset it in the global store.
    if (!order || successPay) {
          // first we clear any existing order (stale state)
      dispatch({ type: ORDER_PAY_RESET });
        // then we add the new order, i.e the one in our address bar
      dispatch(getOrderDetails(orderId));
        // see if its not paid 
    } else if (!order.isPaid) {
  // Once we add the script, we get access to a 'paypal' object
      // on our window, so we'll use that here
      // see if paypal script is loaded. If not
      if (!window.paypal) {
      // add it
        addPayPalScript();
      } else {
        setSdkReady(true);
      }
    }
  }, [dispatch, orderId, successPay, order]);

  const successPaymentHandler = (paymentResult) => {
    console.log('PAYPAL PAYMENT OBJECT', paymentResult);
    dispatch(payOrder(orderId, paymentResult));
  };

  return loading ? (
    <Loader />
  ) : error ? (
    <Message type="error">{error}</Message>
  ) : (
    <>
      <Heading as="h1">Order {order._id}</Heading>
      <Flex w="full" py="5" direction="column">
        <Grid templateColumns="3fr 2fr" gap="20">
          <Flex direction="column">
            <Box borderBottom="1px" py="6" borderColor="gray.300">
              <Heading as="h2" fontSize="2xl" fontWeight="semibold" mb="3">
                Shipping
              </Heading>
              <Text>
                <strong>Name: </strong> {order.user.name}
              </Text>
              <Text>
                <strong>Email: </strong>{' '}
                <a
                  style={{ textDecoration: 'underline' }}
                  href={`mailto:${order.user.email}`}
                >
                  {order.user.email}
                </a>
              </Text>
              <Text mb="3">
                <strong>Address: </strong>
                {order.shippingAddress.address}, {order.shippingAddress.city},{' '}
                {order.shippingAddress.postalCode},{' '}
                {order.shippingAddress.country}
              </Text>
              {order.isDelievered ? (
                <Message type="success">
                  Delievered on {order.delieveredAt}
                </Message>
              ) : (
                <Message type="error">Not Delievered</Message>
              )}
            </Box>

            <Box borderBottom="1px" py="6" borderColor="gray.300">
              <Heading as="h2" fontSize="2xl" fontWeight="semibold" mb="3">
                Payment Method
              </Heading>
              <Text mb="3">
                <strong>Method:</strong> {order.paymentMethod}
              </Text>
              {order.isPaid ? (
                <Message type="success">Paid on {order.paidAt}</Message>
              ) : (
                <Message type="error">Not Paid</Message>
              )}
            </Box>

            <Box borderBottom="1px" py="6" borderColor="gray.300">
              <Heading as="h2" fontSize="2xl" fontWeight="semibold" mb="3">
                Order Items
              </Heading>
              <Box>
                {order.orderItems.length === 0 ? (
                  <Message>Order is empty</Message>
                ) : (
                  <Box py="2">
                    {order.orderItems.map((item, index) => (
                      <Flex
                        key={index}
                        alignItems="center"
                        justifyContent="space-between"
                      >
                        <Flex py="2" alignItems="center">
                          <Image
                            src={item.image}
                            alt={item.name}
                            w="12"
                            h="12"
                            objectFit="cover"
                            mr="6"
                          />
                          <Link
                            as={RouterLink}
                            to={`/product/${item.product}`}
                            fontWeight="medium"
                            fontSize="xl"
                          >
                            {item.name}
                          </Link>
                        </Flex>
                        <Text fontSize="lg" fontWeight="semibold">
                          {item.qty || 1} x ₹{item.price} = ₹
                          {(item.qty || 1) * item.price}
                        </Text>
                      </Flex>
                    ))}
                  </Box>
                )}
              </Box>
            </Box>
          </Flex>

          <Flex
            direction="column"
            bgColor="white"
            justifyContent="space-between"
            py="8"
            px="8"
            shadow="md"
            rounded="lg"
            borderColor="gray.300"
          >
            <Box>
              <Heading mb="6" as="h2" fontSize="3xl" fontWeight="bold">
                Order Summary
              </Heading>
              {/* Item prices */}
              <Flex
                borderBottom="1px"
                py="2"
                borderColor="gray.200"
                alignItems="center"
                justifyContent="space-between"
              >
                <Text fontSize="xl">Items</Text>
                <Text fontWeight="bold" fontSize="xl">
                  ₹{order.itemsPrice}
                </Text>
              </Flex>
              {/* Shipping price */}
              <Flex
                borderBottom="1px"
                py="2"
                borderColor="gray.200"
                alignItems="center"
                justifyContent="space-between"
              >
                <Text fontSize="xl">Shipping</Text>
                <Text fontWeight="bold" fontSize="xl">
                  ₹{order.shippingPrice}
                </Text>
              </Flex>
              {/* Tax price */}
              <Flex
                borderBottom="1px"
                py="2"
                borderColor="gray.200"
                alignItems="center"
                justifyContent="space-between"
              >
                <Text fontSize="xl">Tax</Text>
                <Text fontWeight="bold" fontSize="xl">
                  ₹{order.taxPrice}
                </Text>
              </Flex>
              {/* Total price */}
              <Flex py="2" alignItems="center" justifyContent="space-between">
                <Text fontSize="xl">Total</Text>
                <Text fontWeight="bold" fontSize="xl">
                  ₹{order.totalPrice}
                </Text>
              </Flex>
            </Box>

            {/* Will add a paypal button here */}
            {!order.isPaid && (
              <Box>
                {loadingPay && <Loader />}
                {!sdkReady ? (
                  <Loader />
                ) : (
                  <PayPalButton
                    amount={order.totalPrice}
                    onSuccess={successPaymentHandler}
                  />
                )}
              </Box>
            )}
          </Flex>
        </Grid>
      </Flex>
    </>
  );
};

export default OrderScreen;