// import { writeFile } from 'node:fs/promises';
import { extname } from 'path';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

/** @type {import('./$types').Actions} */
const s3 = new S3Client({
  region: 'us-west-2',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    sessionToken: process.env.AWS_SESSION_TOKEN
  }
});

export const actions = {
  default: async ({ request }) => {
    const formData = await request.formData();
    const uploadedFile = formData?.get('file');
    const originalFilename = uploadedFile?.name;
    const s3Location = `${crypto.randomUUID()}${extname(originalFilename)}`;
    const fileDescription = formData?.get('description');
    const bucketName = 'nivalta-health';

    const flaskParams = {
      name: originalFilename,
      description: fileDescription,
      s3Location: s3Location,
    }

    const params = {
      Bucket: bucketName,
      Key: s3Location,
      Body: Buffer.from(await uploadedFile?.arrayBuffer()),
      ContentType: uploadedFile?.type
    };
    console.log(params);
    
    try {
      await s3.send(new PutObjectCommand(params));
      return { success: true, flaskParams };
    } catch (error) {
      console.error('Error uploading file:', error);
      return { success: false, error: 'Failed to upload file' };
    }
  }
};