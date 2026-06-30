package com.tarea4.tarea4.models;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "miembro")
public class Miembro {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String nombres;

    private String apellidos;

    private String correo;

    private String telefono;

    @Column(name = "tipo_miembro")
    private String tipoMiembro;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "comuna_id")
    private Comuna comuna;

    @Column(name = "fecha_registro")
    private LocalDateTime fechaRegistro;

    public Integer getId() {
        return id;
    }

    public String getNombres() {
        return nombres;
    }

    public String getApellidos() {
        return apellidos;
    }

    public String getCorreo() {
        return correo;
    }

    public String getTelefono() {
        return telefono;
    }

    public String getTipoMiembro() {
        return tipoMiembro;
    }

    public Comuna getComuna() {
        return comuna;
    }

    public LocalDateTime getFechaRegistro() {
        return fechaRegistro;
    }

    public String getNombreCompleto() {
        return nombres + " " + apellidos;
    }
}