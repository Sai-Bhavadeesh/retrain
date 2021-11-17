import { Form, Button } from "react-bootstrap";

const AddNewProduct = () => {
  return (
    <div>
      <h3>Adding New Product Details</h3>
      <Form style={{ paddingRight: "35%" }}>
        <Form.Group className="mb-3" controlId="color">
          <Form.Label>Color of the Box</Form.Label>
          <Form.Control type="text" placeholder="Enter color of the box" />
        </Form.Group>
        <Form.Group className="mb-3" controlId="dashboard">
          <Form.Label>Dashboard Name</Form.Label>
          <Form.Control type="text" placeholder="Enter dashboard name" />
        </Form.Group>
        <Form.Group className="mb-3" controlId="sizzli">
          <Form.Label>Sizzli Box Name</Form.Label>
          <Form.Control type="text" placeholder="Enter sizzli box name" />
        </Form.Group>
        <Button variant="primary" type="submit">
          Save
        </Button>
      </Form>
    </div>
  );
};

export default AddNewProduct;
