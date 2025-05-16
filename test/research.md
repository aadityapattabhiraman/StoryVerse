# StoryVerse Research

## TODO

* [x] API rate limits, RPM ,cost
* [ ] Fall back API/method
* [x] Database (size/type of data to be stored/maintenance)-books,photos,user data
* [ ] Request queueing mechanism
* [ ] Azure VM vs Azure services cost and effort (load balancing/scaling/maintaining redis/database)
* [ ] CPU/GPU/RAM requirements for 1000 user site
* [x] Payment handling

### API Rate Limits, Cost

* All Azure pricing is with respect to 100 images
* Go through Chatgpt Usage Tiers as well

Reference: 
* [Rate Limits](https://platform.openai.com/settings/organization/limits) 
* [Cost](https://platform.openai.com/docs/pricing)
* [Azure](https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits?tabs=REST#batch-limits)

#### Dall-e-2

* OpenAI

    * 500 Requests per minute or 5 images per minute (whichever occurs first)

    * Pricing

    * Standard Quality
        * 256x256   -> $0.016
        * 512x512   -> $0.018
        * 1024x1024 -> $0.02

* Azure

    * Default DALL-E 2 -> 2 concurrent requests
    
    * Pricing
        
        * Standard
            * 1024x1024 -> $2
    
#### Dall-e-3

* OpenAI 

    * 500 Requests per minute or 5 images per minute (whichever occurs first)

    * Pricing

        * Standard Quality
            * 1024x1024 -> $0.04
            * 1024x1792 -> $0.08
            * 1792x1024 -> $0.08

        * HD Quality
            * 1024x1024 -> $0.08
            * 1024x1792 -> $0.12
            * 1792x1024 -> $0.12

* Azure

    * Default DALL-E 3 -> 2 capacity units (6 requests per minute)

    * Pricing

        * Standard Quality
            * 1024x1024 -> $4
            * 1024x1792 -> $8
            * 1792x1024 -> $8

        * HD Quality
            * 1024x1024 -> $8
            * 1024x1792 -> $12
            * 1792x1024 -> $12

#### gpt-image-1

* OpenAI

    * 40000 tokens per minute or 5 images per minute (whichever occurs first)

    * Pricing

    * Low Quality
        * 1024x0124 -> $0.011
        * 1024x1536 -> $0.016
        * 1536x1024 -> $0.016

    * Medium Quality
        * 1024x0124 -> $0.042
        * 1024x1536 -> $0.063
        * 1536x1024 -> $0.063

    * High Quality
        * 1024x0124 -> $0.167
        * 1024x1536 -> $0.25
        * 1536x1024 -> $0.25

    * Please note that this pricing for GPT Image 1 does not include text and image tokens used in the image generation process, and only reflects the output image tokens cost. There are no additional costs for DALL·E 2 or DALL·E 3.

* Azure

    * Default GPT-image-1 -> 2 capacity units (6 requests per minute)
    
    * No pricing information has been specified anywhere

### Fallback API or Method

### Database

* We can use non relational database to store unstructured data related to the user as to their identification.
* We can either store the images in binary format in no-sql which is not recommended or use a hybrid approach.
* The hybrid approach being use no-sql to store most of the information related to user and stuff like images and books can be stored in (e.g) azure blob and the link to the azure blob is stored in the no-sql db for easy access.
* [MongoDB](https://www.mongodb.com/docs/atlas/cluster-autoscaling/)
* [CosmosDB](https://learn.microsoft.com/en-us/azure/cosmos-db/introduction)

#### Mongodb, Azure Cosmosdb (No-SQL)

* We already have access to mongodb atlas that can be deployed to azure, or use azure based cosmosdb as well.
* Mongodb can also be deployed by us if we need full control.
* Mongodb requires manual configuration for efficient scaling.
* Cosmosdb has many options for api including mongodb and others. 
* Cosmosdb is fully automatic scaling
* Data stored is going to be images, books, user specific data

#### Azure Blob

* images, books and other large data

### Payment 

#### Payment Gateways

* paypal
* godaddy
* stripe
* square
* razorpay

### Azure VM v/s Services

* [Azure Services](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/load-balancing-overview)
* [VMSS](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview)

#### VM 

* Number of VM instances can automatically increased or decreased based on demand using VMSS
* Charged based on servers allocated.

#### Azure Managed Services

* Deploy apps [Azure Web App](https://azure.microsoft.com/en-us/products/app-service/web)
* Web app is for frontend or backend. It can scale out and in as per the demand.
* It can only run 1 language at a time.
* Cost is based on usage.
* Functions App [Azure Functions App](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview)
* Functions app is more for backend where if event is triggered it will perform a function.
* It is serverless and priced based on usage.
* It can run only 1 language at a time.

