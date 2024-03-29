import asyncHandler from 'express-async-handler';
import Product from '../models/productModel.js';

const getProducts = asyncHandler(async (req,res) => {
    const products = await Product.find({
        "latestProduct": true
      })
    res.json(products);
});

const getProductById = asyncHandler( async (req,res) => {
    console.log(req.params.id)
    const product = await Product.findById(req.params.id);
    
    if (product){
        res.json(product);
    } else {
        throw new Error('Product not found')
    }
 } 
)

export {getProducts, getProductById};