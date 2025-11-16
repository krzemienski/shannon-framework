# E-Commerce Platform

Build a full-stack e-commerce platform for online retail.

## Frontend Requirements

- **React** application with TypeScript
- **Product Catalog**: Browse products with filtering (category, price range, ratings)
- **Product Details**: View product images, descriptions, reviews, specifications
- **Shopping Cart**: Add/remove items, update quantities, view total with tax
- **Checkout Flow**: Multi-step checkout (shipping, payment, confirmation)
- **User Account**: Login, registration, profile management, order history
- **Admin Dashboard**: Manage products, view orders, update inventory
- **Responsive Design**: Mobile-first approach with desktop optimization

## Backend Requirements

- **Express API** with TypeScript
- **Authentication**: JWT-based auth with refresh tokens
- **Authorization**: Role-based access (customer, admin)
- **Product API**: CRUD operations, search, filtering
- **Cart API**: Session-based cart management
- **Order API**: Order creation, payment processing, status tracking
- **Payment Integration**: Stripe for credit card processing
- **Email Service**: SendGrid for order confirmations, receipts

## Database Requirements

- **PostgreSQL** for relational data
- **Schema**: Users, products, orders, order_items, reviews, inventory tables
- **Migrations**: Version-controlled schema migrations
- **Indexing**: Optimized queries for product search and filtering
- **Constraints**: Foreign keys, unique constraints, data integrity

## Infrastructure

- **Docker**: Containerized application
- **Environment**: Development, staging, production configurations
- **Deployment**: AWS (ECS or similar)
- **CI/CD**: Automated testing and deployment pipeline
- **Monitoring**: Basic error logging and performance monitoring

## Success Criteria

- Users can browse, search, and purchase products end-to-end
- Admin can manage inventory and fulfill orders
- Payment processing is secure and reliable (PCI compliance)
- System handles 100+ concurrent users
- 99.9% uptime target
