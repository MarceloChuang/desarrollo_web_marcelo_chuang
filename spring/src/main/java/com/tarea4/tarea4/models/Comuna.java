package com.tarea4.tarea4.models;

import jakarta.persistence.*;

@Entity
@Table(name = "comuna")
public class Comuna {

    @Id
    private Integer id;

    @Column(nullable = false, length = 200)
    private String nombre;

    @Column(name = "region_id", nullable = false)
    private Integer regionId;

    public Integer getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public Integer getRegionId() {
        return regionId;
    }
}